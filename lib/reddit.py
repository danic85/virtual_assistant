#!/usr/bin/python
# -*- coding: latin-1 -*-
# Source: https://github.com/xDHILEx/Shower-Thoughts/blob/master/Reddit.py

from random import randint
from json import load
from urllib2 import urlopen

def getJson(url):
    # Returns a JSON object from the URL passed in.
    response = urlopen(url)
    json_obj = load(response)
    return json_obj

def getTitles(json_obj):
    # passing in the json_obj, append the title of each post to titles list, returns titles list.
    titles = []
    for i in json_obj['data']['children']:
    	 titles.append("%s" % i['data']['title'])
    return titles

def rand():
    # returns a random integer between 0 and 24 (Posts #1 - #25 on Reddit)
    return randint(0,24)

def showerthought(self):
    """ returns a (one) random post title """
    URL = "http://www.reddit.com/r/showerthoughts/top/.json"
    titles = getTitles(getJson(URL))

    return titles[rand()]