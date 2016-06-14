#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
import pwd
import grp
import os
from os.path import getmtime
import git
import subprocess

#expenses
import csv

import schedule
import datetime
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
        
        self.user = self.command = False
        self.admin = self.config.get('Config', 'Admin')
	self.adminName = self.config.get('Config', 'AdminName')
        if (self.config.get('Config', 'EnableChat') == 1):
            self.chatbot = ChatBot(self.config.get('Config', 'Name'))
            self.chatbot.train("chatterbot.corpus.english")
            
        
        self.last_mtime = os.path.getmtime(__file__)
        print("Version: " + str(self.last_mtime))
        #print(self.getMe())
        
        

    # Handle messages from users
    def handle(self, msg):
        self.adminMessage(msg['chat']['id'])
        self.adminMessage(self.config.get('Config','Users').split(','))
        try:
            if msg['chat']['id'] not in self.config.get('Config','Users').split(','):
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
		if(self.config.get('Config','EnableChat') == 1):
	        	response = self.chatbot.get_response(command)
		else:
			response = "I don't understand, user: " + self.user
        
    	if response != '':
		self.message(response)
	self.command = self.user = False
        
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
            return e 
        print 'No match' 
        return False

    def morning(self):
	response = 'Good morning ' + self.adminName + ' it is ' + self.time() + '\n\n'
	response += self.weather() + '\n\n'
	response += self.word_of_the_day() + '\n\n'
	response += self.news()
	return response

    def time(self):
	return datetime.datetime.now().strftime('%I:%M %p')

    def command_list(self):
        response = "Available commands:\n"
    
        for key, val in self.commandList:
            response += key + "\n"
        print response
        return response

    def weather(self):
        return lib.weather.weather_openweathermap(self, self.config.get('Config', 'OpenWeatherMapKey'))
        
    def word_of_the_day(self):
        return lib.word_of_the_day.word_of_the_day()
        
    def check_fibre_status(self):
        #self.message('Checking fibre status...')
        return lib.fibre_checker.check(self.config.get('Config', 'FibreTel'))
    
    def news(self):
        return lib.news.top_stories(10)
       
    def take_photo(self):
        response = lib.camera.snap()
        if response:
            return response
        f = open('image.jpg', 'rb')  # file on local disk
        response = bot.sendPhoto(self.admin, f) # only send to admin (for security)
        os.remove('image.jpg') # don't save it!
        return ''

    def take_video(self):
        response = lib.camera.video()
        if response:
           return response
        
        p = subprocess.Popen('MP4Box -add video.h264 video.mp4', stdout=subprocess.PIPE, shell=True)
        for line in p.communicate():
             print line
        p.wait()
        print p.returncode
        
        f = open('video.mp4', 'rb')
        response = bot.sendVideo(self.admin, f)
        os.remove('video.mp4')
        os.remove('video.h264')

        return ''

    def update_self(self):
        # pull from git
        directory = os.path.dirname(os.path.realpath(__file__))
        g = git.cmd.Git(directory)
        g.pull()
        
        # Update owner of files to prevent permission issues
        uid = pwd.getpwnam("pi").pw_uid
        gid = grp.getgrnam("pi").gr_gid
        for root, dirs, files in os.walk(directory):  
          for momo in dirs:  
            os.chown(os.path.join(root, momo), uid, gid)
          for momo in files:
            os.chown(os.path.join(root, momo), uid, gid)
        
        # Check if the file has changed.
        # If so, restart the application.
        if os.path.getmtime(__file__) > self.last_mtime:
            # Restart the application (os.execv() does not return).
            self.restart_self()
            
        return 'Updated to version: ' + str(self.last_mtime)
    def restart_self(self):
        print('restarting')
        os.execv(__file__, sys.argv)

    def expenses_remaining(self):
        remaining = 0.0;
        with open('expenses.csv', 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                remaining += float(row[1].strip())
        return 'There is £' + str(format(remaining, '.2f')) + ' left this month.';

    def expenses_add(self):
        self.user = self.config.get('Config','Users').split(',')
        expense = self.command.split(' ', 1)
        with open('expenses.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow([expense[1], float(expense[0].strip()) * -1, datetime.datetime.now()])
        return 'Logged expense: ' + str(self.command) + "\n" + self.expenses_remaining()
        
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
schedule.every().day.at("17:15").do(execute_bot_command, 'weather')

# If method call defined on launch, call. Else listen for commands from telegram
if len(sys.argv) == 2:
    execute_bot_command(sys.argv[1])
else:
    bot.listen()
