#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
import logging
import os
import schedule
import time
import telepot
import datetime
import traceback
import lib
from db import Database

from behaviours import *
from interaction import Interaction

if sys.version_info < (3,0):
    import ConfigParser
else:
    import configparser

# if sys.version_info < (3,0):
#     import aiml

logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__)) + '/files/mojo_debug.log', level=logging.DEBUG)

class Mojo(telepot.Bot):
    """The Bot Object that handles interactions and passes them to the behaviours for processing

        Extends Telegram Bot

        Attributes:
            logging: logging object
            behaviours: an object containing lists of behaviours, keyed by execution order
            dir: path to application directory
            files: path to application files directory
            config: config key: value pairs
            admin: telegram ID of admin account

    """

    def __init__(self, *args, **kwargs):
        """ Initialise attributes and register all behaviours """
        self.logging = logging
        self.__log('Starting Mojo')
        self.db = Database()
        self.mode = 'telegram'

        self.behaviours = {}

        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.files = self.dir + '/files'

        if sys.version_info < (3, 0):
            self.config = ConfigParser.ConfigParser()
        else:
            self.config = configparser.ConfigParser()
        self.config.read(self.dir + "/config.ini")

        super(Mojo, self).__init__(self.config.get('Config', 'Telbot'), **kwargs)

        self.admin = self.config.get('Config', 'Admin')

        self.last_mtime = os.path.getmtime(__file__)  # @todo remove and use git sha instead for update script
        self.__log("Version: " + str(self.last_mtime))

        self.register_behaviours()

    def register_behaviours(self):
        """ Instantiate and create reference to all behaviours as observers """
        dir_path = self.dir + '/behaviours'
        for path, subdirs, files in os.walk(dir_path):
            for name in files:
                if name.endswith('.py') and '__' not in name and name != 'behaviour.py' and 'test_' not in name:
                    m = name.split('.')[0]
                    instance = getattr(globals()[m], m.title())(db=self.db, config=self.config, dir=self.dir,
                                                                logging=logging)  # Get instance of class

                    # Add to behaviours list in order of execution
                    if instance.execution_order not in self.behaviours:
                        self.behaviours[instance.execution_order] = []
                    self.behaviours[instance.execution_order].append(instance)

    def listen(self, **kwargs):
        """ Handle messages via telegram and run scheduled tasks """
        self.mode = kwargs.get('mode', 'telegram')
        if self.mode == 'telegram':
            self.message_loop(self.handle)
            self.__admin_message('Hello!')

        self.__log('Listening ...')

        # Keep the program running.
        while 1:
            if self.mode == 'console':
                self.console_input()
            schedule.run_pending()
            self.__idle_behaviours()
            time.sleep(1)

    def console_input(self):
        if sys.version_info < (3, 0):
            command = raw_input("Enter command: ")
        else:
            command = input("Enter command: ")
        print(command)
        self.handle({"chat": {"id": self.admin}, "text": command, "console": True})

    def handle(self, msg):
        """ Handle messages from users (must be public for telegram) """
        if 'voice' in msg:
            msg['text'] = lib.speech.get_message(self, msg)

        if 'text' in msg:
            self.__log(self.__datetime() + ': Message received: ' + msg['text'])
        try:
            if str(msg['chat']['id']) not in self.config.get('Config', 'Users').split(','):
                self.__admin_message('Unauthorized access attempt by: ' + str(msg['chat']['id']))
                return
        except Exception as e:
            self.__admin_message(str(e))
            msg['chat']['id'] = self.admin

        act = Interaction(user=[msg['chat']['id']],
                          command={'text': msg['text'].strip()},
                          config=self.config)

        self.__log(act.command['text'])

        act = self.__interact(act)

        if len(act.response) > 0:
            if 'voice' in msg:
                # Respond with voice if audio input received
                lib.speech.speak(self, act.get_response_str())
                self.sendAudio(act.user, open(self.files + '/speech/output.mp3'))
            elif 'console' in msg:
                # Just print response if was sent from a console command
                self.__log(act.get_response_str())
            else:
                # Standard text response via telegram
                self.__message(act)

            # Handle chained commands
            for r in act.response:
                if 'command' in r:
                    print("I think theres another command: " + str(r))
                    new_cmd = {'text': r['command']['text'], 'chat': {'id': act.user[0]}}
                    if 'console' in msg:
                        new_cmd['console'] = True
                    self.handle(new_cmd)

    def __idle_behaviours(self):
        """ Call idle method for each behaviour """
        act = self.__interact(Interaction(user=[self.admin], config=self.config, method='idle'))
        if len(act.response) > 0:
            self.__message(act)

    def __interact(self, act):
        """ Send interaction to behaviours, in order of execution.
            Stop when response returned if act.finish == True
        """
        if act.method != 'idle':
            self.__log('Received command: ' + act.command['text'])

        try:
            # Try observers first
            for ex_order in self.behaviours:
                for behaviour in self.behaviours[ex_order]:
                    r = getattr(behaviour, act.method)(act)  # call method specified in interaction object
                    if r is not None:
                        act.respond(r)
                if len(act.response) > 0 and act.finish:
                    break

        except Exception as e:
            template = "An exception of type {0} occurred with the message '{1}'. Arguments:\n{2!r}"
            message = template.format(type(e).__name__, str(e), e.args)
            print(traceback.print_tb(e.__traceback__))
            self.__log(message)
            act.respond(message)
            return act

        if len(act.response) == 0 and act.method != 'idle':
            self.__log('No match')
            act.respond("I'm sorry I don't know what to say")
        return act

    def __message(self, act):
        """ Parse interaction object and convert to user friendly response message """
        msg = act.get_response_str()

        if self.mode == 'console':
            self.__log(msg)
            return

        if act.user:
            for u in act.user:
                self.__log('sending to' + str(u))
                self.sendMessage(u, msg, None, True)
        else:
            self.__admin_message(msg)

        files = act.get_response_files()
        if len(files) > 0:
            for f in files:
                if f['file'] == 'photo':
                    photo = open(f['path'], 'rb')
                    for u in act.user:
                        self.__log('sending photo to' + str(u))
                        self.sendPhoto(u, photo)
                    os.remove(photo)
                if f['file'] == 'video':
                    video = open(f['path'], 'rb')
                    for u in act.user:
                        self.__log('sending video to' + str(u))
                        self.sendVideo(u, video)
                    os.remove(video)

    def __admin_message(self, msg):
        if self.mode == 'console':
            self.__log(msg)
            return
        self.sendMessage(self.admin, msg)

    @staticmethod
    def __log(text):
        """ Output and log text """
        print(Mojo.__datetime() + text)
        logging.info(Mojo.__datetime() + text)

    @staticmethod
    def __datetime():
        """ Return readable datetime """
        return datetime.datetime.now().strftime('%d-%m-%y %I:%M %p - ')
