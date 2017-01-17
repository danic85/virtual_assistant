#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
import logging

import os
import schedule
import time
import re
import telepot
from pprint import pprint
# from chatterbot import ChatBot
import importlib
import aiml

from lib import *

import ConfigParser

logging.basicConfig(filename= os.path.dirname(os.path.realpath(__file__))+'/mojo_debug.log',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

class Mojo(telepot.Bot):
    def __init__(self, *args, **kwargs):
        self.logging = logging
        logging.info('Starting Mojo');
        self.config = ConfigParser.ConfigParser()
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.files = self.dir + '/files'
        conf =  self.dir + "/config.ini"
        print conf
        self.config.read(conf)
        
        # Parse commands
        p = ConfigParser.ConfigParser()
        c = self.dir + "/commands.ini"
        p.read(c)
        self.commandList = p.items('Commands');
        
        super(Mojo, self).__init__(self.config.get('Config', 'Telbot'), **kwargs)
        
        self.user = self.command = False
        self.admin = self.config.get('Config', 'Admin')
        self.adminName = self.config.get('Config', 'AdminName')

        if (self.config.get('Config', 'EnableChat') == '1'):
            print 'chatbot enabled'
            self.chat = aiml.Kernel()

            if os.path.isfile(self.files + "/bot_brain.brn"):
                self.chat.bootstrap(brainFile = self.files + "/bot_brain.brn")
            else:
                self.chat.bootstrap(learnFiles = self.files + "/aiml/*", commands = "load aiml b")
                self.chat.saveBrain(self.files + "/bot_brain.brn")
        
        security.init(self)
        
        self.last_mtime = os.path.getmtime(__file__)
        print("Version: " + str(self.last_mtime))

    # Handle messages from users
    def handle(self, msg):
        logging.info(general.date_time(self) + ': Message received: ' + msg['text'])
        try:
            if str(msg['chat']['id']) not in self.config.get('Config','Users').split(','):
                self.adminMessage('Unauthorized access attempt by: ' + str(msg['chat']['id']))
                return
        except Exception as e:
            self.adminMessage(str(e))
            msg['chat']['id'] = self.admin
        
        self.user = msg['chat']['id']
        command = msg['text'].lower().strip()
        
        response = False
        
        # check command list
        response = self.doCommand(command)
        # get a response from chat
        if (not response and response != ''):
            try:
                if(self.config.get('Config','EnableChat') == '1'):
                    print('chatbot response:')
                    response = str(self.chat.respond(command, self.admin))
                    print(response)
                    if (response == ''):
                        response = "I'm sorry, I don't understand"
                else:
                    response = "I'm sorry, I don't understand"
            except Exception as e:
                self.adminMessage(str(e))
        if response != '':
            self.message(response)
        self.command = self.user = False
        
    # Listen
    def listen(self):
        self.message_loop(self.handle)

        print 'Listening ...'
        
        try:
            self.adminMessage(self.chat.respond('hello', self.admin))
        except Exception as e:
            self.adminMessage('Hello!', self.admin)

        # Keep the program running.
        while 1:
            schedule.run_pending()
            security.sweep(self)
            time.sleep(1)
            
    def message(self, msg):
        if (self.user):
            if type(self.user) is list:
                for u in self.user:
                        print 'sending to'
                        print u
                        self.sendMessage(u, msg)
            else:
                self.sendMessage(self.user, msg)
        else:
            self.adminMessage(msg)
        
    def adminMessage(self, msg):
        self.sendMessage(self.admin, msg)
        
    def setAdminId(self, admin):
        self.admin = admin

    def doCommand(self, command):
        print 'Received command: ' + command
        try:
            self.command = command
            for theRegex,theMethod in self.commandList:
                if (re.search(theRegex, command, flags=0)):
                    logging.info('Match on ' + theRegex)
                    
                    if "." in theMethod: 
                        mod_name, func_name = theMethod.rsplit('.',1)
                        mod = importlib.import_module('lib.'+ mod_name)
                        func = getattr(mod, func_name)
                        return func(self)
                    else:
                        func = getattr(self, theMethod)
                        return func()
                    
        except Exception as e:
            print e
            logging.info(e)
            return str(e) 
        print 'No match'
        logging.info('No match')
        return False

    # @todo Refactor to remove these methods
    def update_self(self):
        return general.update_self(self, __file__)
        
bot = Mojo()

def execute_bot_command(command):
    global bot
    print 'jobbing ' + command
    msg = {"chat" : {"id" : bot.admin}, "text" : command}
    print bot.handle(msg)
    
def execute_bot_command_monthly(command):
    now = datetime.datetime.now()
    if (now.day == 1):
        return execute_bot_command(command)

# Load scheduled tasks
schedule.clear()
# schedule.every().minute.do(execute_bot_command, 'is house empty')
schedule.every().day.at("6:30").do(execute_bot_command, 'morning')
schedule.every().day.at("8:30").do(execute_bot_command, 'morning others')
schedule.every().monday.at("8:00").do(execute_bot_command, 'check fibre')
schedule.every().day.at("8:00").do(execute_bot_command_monthly, '700 budget') #reset budget at beginning of month

# If method call defined on launch, call. Else listen for commands from telegram
if len(sys.argv) == 2:
    execute_bot_command(sys.argv[1])
else:
    bot.listen()
