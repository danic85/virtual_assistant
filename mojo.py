#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
import logging
import os
import schedule
import time
import datetime
import re
import telepot
import importlib
import aiml

from lib import *

from db import Database

import ConfigParser

logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__)) + '/files/mojo_debug.log', level=logging.DEBUG)


# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')


class Mojo(telepot.Bot):
    def __init__(self, *args, **kwargs):
        self.logging = logging
        logging.info('Starting Mojo')
        self.config = ConfigParser.ConfigParser()
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.files = self.dir + '/files'
        conf = self.dir + "/config.ini"
        self.config.read(conf)

        # Parse commands
        p = ConfigParser.ConfigParser()
        c = self.dir + "/commands.ini"
        p.read(c)
        self.commandList = p.items('Commands')

        super(Mojo, self).__init__(self.config.get('Config', 'Telbot'), **kwargs)

        self.user = self.command = False
        self.admin = self.config.get('Config', 'Admin')
        self.adminName = self.config.get('Config', 'AdminName')
        self.monzo_tokens = []

        self.chat = aiml.Kernel()

        if os.path.isfile(self.files + "/bot_brain.brn"):
            self.chat.bootstrap(brainFile=self.files + "/bot_brain.brn")
        else:
            self.chat.bootstrap(learnFiles=self.files + "/aiml/*", commands="load aiml b")
            self.chat.saveBrain(self.files + "/bot_brain.brn")

        security.init(self)
        monzo.init(self)

        self.last_mtime = os.path.getmtime(__file__)
        logging.info("Version: " + str(self.last_mtime))

        self.db = Database()

    # Handle messages from users
    def handle(self, msg):
        if 'text' in msg:
            logging.info(general.date_time(self) + ': Message received: ' + msg['text'])
        try:
            if str(msg['chat']['id']) not in self.config.get('Config', 'Users').split(','):
                self.admin_message('Unauthorized access attempt by: ' + str(msg['chat']['id']))
                return
        except Exception as e:
            self.admin_message(str(e))
            msg['chat']['id'] = self.admin

        self.user = msg['chat']['id']
        self.original_message = msg['text'].strip()
        logging.info(msg)
        if 'text' in msg:
            command = msg['text'].lower().strip()
        elif 'voice' in msg:
            command = speech.getMessage(self, msg)
        else:
            return
        response = False

        # check command list
        response = self.do_command(command)
        # get a response from chat
        if not response and response != '':
            try:
                logging.info('chatbot response:')
                response = str(self.chat.respond(command, self.admin))
                logging.info(response)
                if response == '':
                    response = "I'm sorry, I don't understand"
            except Exception as e:
                self.admin_message(str(e))
        if response != '':
            if 'voice' in msg:
                # Respond with voice if audio input received
                speech.speak(self, response)
                self.sendAudio(self.admin, open(self.files + '/speech/output.mp3'))
            elif 'console' in msg:
                # Just print response if was sent from a console command
                print response
            else:
                # Standard text response via telegram
                self.message(response)
        self.command = self.user = False

    # Listen
    def listen(self):
        self.message_loop(self.handle)

        print 'Listening ...'

        try:
            self.admin_message(self.chat.respond('hello', self.admin))
        except Exception as e:
            self.admin_message('Hello!', self.admin)

        # Keep the program running.
        while 1:
            schedule.run_pending()
            time.sleep(1)

    def message(self, msg):
        if self.user:
            if type(self.user) is list:
                for u in self.user:
                    print 'sending to'
                    print u
                    self.sendMessage(u, msg, None, True)
            else:
                self.sendMessage(self.user, msg, None, True)
                if self.config.get('Config', 'BraillespeakPort'):
                    braillespeak.speak(self, msg)
        else:
            self.admin_message(msg)

    def admin_message(self, msg):
        self.sendMessage(self.admin, msg)

    def do_command(self, command):
        print 'Received command: ' + command
        try:
            self.command = command
            for theRegex, theMethod in self.commandList:
                if re.search(theRegex, command, flags=0):
                    logging.info('Match on ' + theRegex)

                    if "." in theMethod:
                        mod_name, func_name = theMethod.rsplit('.', 1)
                        mod = importlib.import_module('lib.' + mod_name)
                        func = getattr(mod, func_name)
                        return func(self)
                    else:
                        func = getattr(self, theMethod)
                        return func()

        except Exception as e:
            template = "An exception of type {0} occured with the message '{1}'. Arguments:\n{2!r}"
            message = template.format(type(e).__name__, str(e), e.args)
            print message
            logging.info(message)
            return str(message)
        print 'No match'
        logging.info('No match')
        return False


def execute_bot_command_console(bot, command):
    msg = {"chat": {"id": bot.admin}, "text": command, "console": True}
    bot.handle(msg)


def execute_bot_command(bot, command):
    msg = {"chat": {"id": bot.admin}, "text": command}
    bot.handle(msg)


def execute_bot_command_monthly(bot, command):
    now = datetime.datetime.now()
    if now.day == 1:
        execute_bot_command(bot, command)

# If method call defined on launch, call. 'startx' = listen for commands from telegram
if len(sys.argv) == 2:
    # Start mojo
    if sys.argv[1] == 'startx':
        bot = Mojo()
        # Load scheduled tasks
        schedule.clear()
        # schedule.every().minute.do(execute_bot_command, 'is house empty')
        schedule.every(10).minutes.do(execute_bot_command, bot, 'get recent transactions')
        schedule.every().day.at("00:00").do(execute_bot_command, bot, 'rotate log')
        schedule.every().day.at("6:30").do(execute_bot_command, bot, 'morning')
        schedule.every().day.at("8:30").do(execute_bot_command, bot, 'morning others')
        schedule.every().day.at("13:00").do(execute_bot_command, bot, 'new houses')
        # schedule.every().monday.at("8:00").do(execute_bot_command, bot, 'check fibre')
        schedule.every().day.at("7:00").do(
            execute_bot_command_monthly,
            bot,
            '-700 budget')  # reset budget at beginning of month
        bot.listen()
    # Execute command without listening (ignore discover unittest)
    elif sys.argv[1] != 'discover':
        bot = Mojo()
        execute_bot_command_console(bot, sys.argv[1])

