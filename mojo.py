#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys

import schedule
import time
import re
import telepot
from pprint import pprint
from chatterbot import ChatBot

import lib
import lib.weather
import lib.word_of_the_day
import lib.fibre_checker
import lib.news
import lib.camera
import lib.expenses
import lib.general

import ConfigParser



class Mojo(telepot.Bot):
    def __init__(self, *args, **kwargs):
        self.config = ConfigParser.ConfigParser()
        conf = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
        print conf
        self.config.read(conf)
        
        # Parse commands
        p = ConfigParser.ConfigParser()
        c = os.path.dirname(os.path.realpath(__file__)) + "/commands.ini"
        p.read(c)
        self.commandList = p.items('Commands');
        
        super(Mojo, self).__init__(self.config.get('Config', 'Telbot'), **kwargs)
        
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.user = self.command = False
        self.admin = self.config.get('Config', 'Admin')
        self.adminName = self.config.get('Config', 'AdminName')
        if (self.config.get('Config', 'EnableChat') == 1):
            self.chatbot = ChatBot(self.config.get('Config', 'Name'))
            self.chatbot.train("chatterbot.corpus.english")
        
        self.last_mtime = os.path.getmtime(__file__)
        print("Version: " + str(self.last_mtime))

    # Handle messages from users
    def handle(self, msg):
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
                if(self.config.get('Config','EnableChat') == 1):
                    response = self.chatbot.get_response(command)
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
        
        self.adminMessage("Hello, I'm here.")

        # Keep the program running.
        while 1:
            schedule.run_pending()
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
                #print theRegex,"=",theMethod
                if (re.search(theRegex, command, flags=0)):
                    print 'Match on ' + theRegex
                    return getattr(self, theMethod)()
        except Exception as e:
            print e
            return str(e) 
        print 'No match' 
        return False

    def morning(self):
        return lib.general.morning(self)

    def time(self):
        return lib.general.time(self)

    def command_list(self):
        return lib.general.command_list(self)

    def weather(self):
        return lib.weather.weather_openweathermap(self, self.config.get('Config', 'OpenWeatherMapKey'))
        
    def word_of_the_day(self):
        return lib.word_of_the_day.word_of_the_day()
        
    def check_fibre_status(self):
        return lib.fibre_checker.check(self.config.get('Config', 'FibreTel'))
    
    def news(self):
        return lib.news.top_stories(10)
       
    def take_photo(self):
        return lib.camera.take_photo(self)

    def take_video(self):
        return lib.camerea.take_video(self)

    def update_self(self):
        return lib.general.update_self(self)
        
    def expenses_remaining(self):
        return lib.expenses.expenses_remaining(self)

    def expenses_add(self):
        return lib.expenses.expenses_add(self)
        
bot = Mojo()

def execute_bot_command(command):
    global bot
    print 'jobbing ' + command
    msg = {"chat" : {"id" : bot.admin}, "text" : command}
    print bot.handle(msg)

# Load scheduled tasks
schedule.clear()
#schedule.every().day.at("2:00").do(execute_bot_command, 'update')
schedule.every().day.at("6:30").do(execute_bot_command, 'morning')
schedule.every().day.at("8:00").do(execute_bot_command, 'check fibre')
schedule.every().day.at("16:30").do(execute_bot_command, 'check fibre')
#schedule.every().day.at("17:15").do(execute_bot_command, 'weather')

# If method call defined on launch, call. Else listen for commands from telegram
if len(sys.argv) == 2:
    execute_bot_command(sys.argv[1])
else:
    bot.listen()
