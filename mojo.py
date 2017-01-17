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

logging.basicConfig(filename='mojo_debug.log',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

class Mojo(telepot.Bot):
    def __init__(self, *args, **kwargs):
        self.logging = logging
        logging.info('Starting Mojo');
        self.config = ConfigParser.ConfigParser()
        conf = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
        print conf
        self.config.read(conf)
        
        self.motionCheckTime = null
        
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

        if (self.config.get('Config', 'EnableChat') == '1'):
            print 'chatbot enabled'
            self.chat = aiml.Kernel()

            if os.path.isfile("bot_brain.brn"):
                self.chat.bootstrap(brainFile = "bot_brain.brn")
            else:
                self.chat.bootstrap(learnFiles = "aiml/*", commands = "load aiml b")
                self.chat.saveBrain("bot_brain.brn")
        
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
        
        self.adminMessage(self.chat.respond('hello', self.admin))

        # Keep the program running.
        while 1:
            schedule.run_pending()
            if (self.motionCheckTime && self.motionCheckTime <= datetime.datetime.now()):
                self.monitor()
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
    def get_weather(self):
        return weather.weather_openweathermap(self, self.config.get('Config', 'OpenWeatherMapKey'))
    def check_fibre_status(self):
        return fibre_checker.check(self.config.get('Config', 'FibreTel'))
    def news(self):
        return news.top_stories(5)
    def take_photo(self):
        return camera.take_photo(self)
    def take_video(self):
        response = lib.camera.video()
        if response:
            return response
        try:
            p = subprocess.Popen('MP4Box -add video.h264 video.mp4', stdout=subprocess.PIPE)
            for line in p.stdout:
                print line
            p.wait()
            print p.returncode
            f = open('video.mp4', 'rb')
            response = bot.sendVideo(self.admin, f)
            os.remove('video.mp4')
            os.remove('video.h264')
        except Exception:
             return 'There was a problem.'
        return ''
    
    def start_monitoring(self):
        interval = self.config.get('Config', 'MotionInterval')
        
        if (self.motionCheckTime != null):
            return 'Already monitoring'
        else:
            self.motionCheckTime = datetime.datetime.now() + datetime.timedelta(seconds=interval)
            self.motionData = lib.camera.getStreamImage(True)

        return 'Started motion sensing'
        
    def monitor(self):
        interval = self.config.get('Config', 'MotionInterval')
	msg = ''
        newData = lib.camera.getStreamImage(True)
        if (checkForMotion(self.motionData, newData)):
            msg = 'Motion detected'
        self.motionCheckTime = datetime.datetime.now() + datetime.timedelta(seconds=interval) 
        self.motionData = newData
        return msg
        
    def stop_monitor(self):
        self.motionData = null
        self.motionCheckTime = null
        return  'Stopped motion sensing'

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
        
    def get_log(self):
        f = open('mojo_debug.log', 'r')
        self.sendDocument(self.user, f)
        return ''
        
    def update_self(self):
        return general.update_self(self, __file__)
    def currency_convert(self):
        return currency.convert(self, 'USD', self.command.replace('convert ',''), self.config.get('Config', 'OpenExchangeRatesKey'))
bot = Mojo()

def execute_bot_command(command):
    global bot
    print 'jobbing ' + command
    msg = {"chat" : {"id" : bot.admin}, "text" : command}
    print bot.handle(msg)

# Load scheduled tasks
schedule.clear()
#schedule.every().day.at("2:00").do(execute_bot_command, 'update')
# schedule.every().minute.do(execute_bot_command, 'is house empty')
schedule.every().day.at("6:30").do(execute_bot_command, 'morning')
schedule.every().day.at("8:30").do(execute_bot_command, 'morning others')
schedule.every().monday.at("8:00").do(execute_bot_command, 'check fibre')
# schedule.every().day.at("16:30").do(execute_bot_command, 'check fibre')
#schedule.every().day.at("17:15").do(execute_bot_command, 'weather')

# If method call defined on launch, call. Else listen for commands from telegram
if len(sys.argv) == 2:
    execute_bot_command(sys.argv[1])
else:
    bot.listen()
