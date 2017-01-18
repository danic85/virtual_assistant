#!/usr/bin/env python
# -*- coding: utf-8 -*-

#riddle
from HTMLParser import HTMLParser
from random import randint

riddles = []
riddle = {}
riddleIndex = 0

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag
        self.currentTag = tag

    def handle_endtag(self, tag):
        # print "Encountered an end tag :", tag
        self.currentTag = ''

    def handle_data(self, data):
        # print "Encountered some data  :", data
        # print "currentTag: " + self.currentTag
        if (self.currentTag == 'em'):
            # print "setting answer"
            self.riddle['answer'] = data
            riddles.append(self.riddle)
        elif (self.currentTag == 'li'):
            # print "setting question"
            self.riddle = {'question': data, 'answer': ''}

def get_riddles(self):
    parser = MyHTMLParser()
    f = open(self.files + '/riddles.htm', 'r')
    parser.feed(f.read().replace('\n',' '))
    return riddles
    
def next(self):
    if (hasattr(self, 'riddles') == False):
        self.riddles = get_riddles(self)
    self.riddleIndex = randint(0, len(self.riddles))            
    return self.riddles[self.riddleIndex]['question']
    
def answer(self):
    if (hasattr(self, 'riddles') == False):
        return
    return self.riddles[self.riddleIndex]['answer']