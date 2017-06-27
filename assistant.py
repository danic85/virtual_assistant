#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime
import logging
import os
import sys
import time
import traceback
import urllib

from PIL import Image
import requests
from io import BytesIO

import schedule
import telepot

import lib
from lib.interaction import Interaction
from lib.db import Database
from lib import config
from responders import console, telegram

from behaviours import *

try:
    logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__)) + '/files/assistant_debug.log', level=logging.DEBUG)
except OSError as ex:
    pass


class Assistant(object):
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
        self.__log('Starting Assistant')
        self.db = Database()
        self.mode = kwargs.get('mode', 'console')

        self.behaviours = {}

        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.files = self.dir + '/files'

        self.config = config.Config()
        self.responder = None

        self.admin = self.config.get_or_request('Admin')

        self.register_behaviours()
        self.register_responders()

        schedule.clear()
        schedule.every(5).minutes.do(self.idle)

    def register_responders(self):
        if self.mode == 'telegram':
            print('loading telegram')
            self.responder = telegram.Telegram(config=self.config)
        else:
            print('loading console')
            self.responder = console.Console(config=self.config)

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

    def listen(self, **kwargs):  # pragma: no cover
        """ Handle messages via telegram and run scheduled tasks """
        self.responder.admin_message('Hello!')
        self.responder.message_loop(self.handle)

        self.__log('Listening ...')

        # Keep the program running.
        while 1:
            if self.mode != 'telegram':
                self.responder.message_loop(self.handle)  # @todo handle in the same way as telegram, with threading
            schedule.run_pending()
            # self.__idle_behaviours()
            time.sleep(1)

    def handle(self, msg):
        """ Handle messages from users (must be public for telegram) """
        text = self.responder.get_text(msg)
        if text == '':
            return

        self.__log(self.__datetime() + ': Message received: ' + text)

        act = Interaction(user=[msg['chat']['id']],
                          command={'text': text.strip()},
                          config=self.config,
                          msg=msg)

        self.__interact(act)

    def idle(self):
        """ Call idle method for each behaviour """
        self.__interact(Interaction(user=[self.admin], config=self.config, method='idle'))

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
            # if self.mode == 'audio':
            print(message)
            print(traceback.print_tb(e.__traceback__))
            self.__log(message)
            act.respond(message)
            return

        if len(act.response) == 0 and act.method != 'idle':
            self.__log('No match')
            act.respond("I'm sorry I don't know what to say")

        # Handle response(s)
        if len(act.response) > 0:
            if act.msg and 'voice' in act.msg:
                # Respond with voice if audio input received
                responses = act.get_response_str()
                for r in responses:
                    lib.speech.speak(self, r['msg'])
                    if self.mode == 'telegram':
                        self.responder.sendAudio(r['user'], open(self.files + '/speech/output.mp3'))
                    else:
                        self.responder.sendAudio(r['user'], self.files + '/speech/output.mp3')
            else:
                # Standard text response via telegram
                self.__message(act)

            # Handle chained commands
            for r in act.response:
                if 'command' in r:
                    # print("I think theres another command: " + str(r))
                    new_cmd = {'text': r['command']['text'], 'chat': {'id': act.user[0]}}
                    self.handle(new_cmd)

    def __message(self, act):
        """ Parse interaction object and convert to user friendly response message """
        responses = act.get_response_str()

        for r in responses:
            msg = r['text']
            if msg != '':
                self.__log(msg)

                if r['user']:
                    for u in r['user']:
                        self.__log('sending to' + str(u))
                        self.responder.sendMessage(u, msg, None, True)

        # @todo modify to handle user in response object
        files = act.get_response_files()
        if len(files) > 0:
            for f in files:
                if f['file'] == 'photo':
                    if 'http' in f['path']:
                        path = self.files + "/temp.jpg"
                        urllib.request.urlretrieve(f['path'], path)
                        f['path'] = path

                    photo = open(f['path'], 'rb')

                    for u in act.user:
                        self.__log('sending photo to' + str(u))
                        self.responder.sendPhoto(u, photo, f['caption'])

                    os.remove(f['path'])

                if f['file'] == 'video':
                    video = open(f['path'], 'rb')
                    for u in act.user:
                        self.__log('sending video to' + str(u))
                        self.responder.sendVideo(u, video)
                    os.remove(video)
                if f['file'] == 'file':
                    doc = open(f['path'], 'rb')
                    for u in act.user:
                        self.__log('sending document to' + str(u))
                        self.responder.sendDocument(u, doc)

    @staticmethod
    def __log(text):
        """ Output and log text """
        logging.info(Assistant.__datetime() + text)

    @staticmethod
    def __datetime():
        """ Return readable datetime """
        return datetime.datetime.now().strftime('%d-%m-%y %I:%M %p - ')
