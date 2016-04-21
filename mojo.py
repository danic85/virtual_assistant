#!/usr/bin/python
import sys
import time
import re
import telepot
from pprint import pprint
from chatterbot import ChatBot
import lib.weather

class Mojo(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(Mojo, self).__init__(*args, **kwargs)
        self.user = ''
        self.chatbot = ChatBot("Mojo")
        self.chatbot.train("chatterbot.corpus.english")
        print(self.getMe())

    # Handle messages from users
    def handle(self, msg):
    	chat_id = msg['chat']['id']
    	command = msg['text']
        
        response = False
        
        # check command list
        response = self.doCommand(command)
        # get a response from chat
        if (not response):
            response = self.chatbot.get_response(command)
        
    	self.sendMessage(chat_id, response)
        
    # Listen (currently not called)
    def listen(self):
        self.message_loop(self.handle)

        print 'Listening ...'

        # Keep the program running.
        while 1:
            time.sleep(1000)
            
    def message(self, msg):
        self.sendMessage(self.user, msg)
        
    def setUserId(self, user):
        self.user = user

    def doCommand(self, command):
        commandList = {"regex1":"command","weather":"weather"}
        for theRegex,theMethod in commandList.iteritems():
            print theRegex,"=",theMethod
            if (re.search(theRegex, command, flags=0)):
                print 'match'
                return getattr(self, theMethod)();
          
        return False
    
    def command(self):
        return "command executed"

    def weather(self):
        return lib.weather.weather_yahoo(self, '2459115','query.yahooapis.com','/v1/public/yql?q=select%%20*%%20from%%20weather.forecast%%20where%%20woeid%%3D',1,'&format=json')

    
TOKEN = sys.argv[1]  # get token from command-line
ME = sys.argv[2]  # get token from command-line
LISTEN = sys.argv[3] # 1 or 0, start listening?

print(LISTEN)

bot = Mojo(TOKEN)
bot.setUserId(ME)

if (LISTEN != '0'):
    bot.listen()
    
