#!/usr/bin/python
import sys
import schedule
import time
import re
import telepot
from pprint import pprint
from chatterbot import ChatBot
import lib.weather
import lib.word_of_the_day
import lib.fibre_checker
import git

import ConfigParser

import os
from os.path import getmtime

class Mojo(telepot.Bot):
    def __init__(self, *args, **kwargs):
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        
        super(Mojo, self).__init__(self.config.get('Config', 'Telbot'), **kwargs)
        
        self.user = ''
        self.admin = self.config.get('Config', 'Admin')
        self.chatbot = ChatBot(self.config.get('Config', 'Name'))
        self.chatbot.train("chatterbot.corpus.english")
        self.commandList = {
                            "list commands|help|command list":"command_list",
                            "weather":"weather",
                            "word of the day":"word_of_the_day",
                            "check fibre":"check_fibre_status",
                            "update":"update_self"
                            }
        self.last_mtime = os.path.getmtime(__file__)
        print("Version: " + str(self.last_mtime))
        #print(self.getMe())
        
        

    # Handle messages from users
    def handle(self, msg):
    	self.user = msg['chat']['id']
    	command = msg['text']
        
        response = False
        
        # check command list
        response = self.doCommand(command)
        # get a response from chat
        if (not response):
            response = self.chatbot.get_response(command)
        
    	self.message(response)
        self.chat_id = False
        
    # Listen
    def listen(self):
        self.message_loop(self.handle)

        print 'Listening ...'

        # Keep the program running.
        while 1:
            schedule.run_pending()
            time.sleep(1)
            
            
    def message(self, msg):
        if (self.user):
            self.sendMessage(self.user, msg)
        else:
            self.adminMessage(msg)
        
    def adminMessage(self, msg):
        self.sendMessage(self.admin, msg)
        
    def setAdminId(self, admin):
        self.admin = admin

    def doCommand(self, command):
        for theRegex,theMethod in self.commandList.iteritems():
            print theRegex,"=",theMethod
            if (re.search(theRegex, command, flags=0)):
                print 'match'
                return getattr(self, theMethod)()
          
        return False
    
    def command_list(self):
        response = "Available commands:\n"
    
        for key, val in self.commandList.iteritems():
            response += key + "\n"
        print response
        return response

    def weather(self):
        return lib.weather.weather_openweathermap(self, self.config.get('Config', 'OpenWeatherMapKey'))
        
    def word_of_the_day(self):
        return lib.word_of_the_day.word_of_the_day()
        
    def check_fibre_status(self):
        self.message('Checking fibre status...')
        return lib.fibre_checker.check(self.config.get('Config', 'FibreTel'))
        
    def update_self(self):
        # pull from git
        g = git.cmd.Git(os.path.dirname(os.path.realpath(__file__)))
        g.pull()
        # Check if the file has changed.
        # If so, restart the application.
        if os.path.getmtime(__file__) > self.last_mtime:
            # Restart the application (os.execv() does not return).
            self.restart_self()
            
        return 'Updated to version: ' + str(self.last_mtime)
    def restart_self(self):
        print('restarting')
        os.execv(__file__, sys.argv)
        
        
bot = Mojo()

def execute_bot_command(command):
    global bot
    print 'jobbing ' + command
    msg = {"chat" : {"id" : bot.admin}, "text" : command}
    print bot.handle(msg)

# Load scheduled tasks
schedule.every().day.at("2:00").do(execute_bot_command, 'update')
schedule.every().day.at("6:30").do(execute_bot_command, 'weather')
schedule.every().day.at("6:30").do(execute_bot_command, 'word of the day')
schedule.every().day.at("8:00").do(execute_bot_command, 'check fibre')
schedule.every().day.at("16:30").do(execute_bot_command, 'check fibre')
schedule.every().day.at("17:15").do(execute_bot_command, 'weather')

bot.listen()