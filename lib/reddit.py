#!/usr/bin/python
# -*- coding: latin-1 -*-
# Source: https://github.com/xDHILEx/Shower-Thoughts/blob/master/Reddit.py

from random import randint
from json import load
import urllib2
from profanity import profanity


def get_json(url):
    """ Requests using custom header to avoid 'HTTP Error 429: Too Many Requests' error """
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    feeddata = opener.open(url)
    return load(feeddata)


def get_titles(json_obj):
    """ Passing in the json_obj, append the title of each post to titles list, returns titles list. """
    titles = []
    for i in json_obj['data']['children']:
        titles.append("%s" % i['data']['title'])
    return titles


def rand():
    """ Returns a random integer between 0 and 24 (Posts #1 - #25 on Reddit) """
    return randint(0, 24)


def get_random_title(self, url):
    """ Returns a (one) random post title """
    try:

        titles = get_titles(get_json(url))
        post = titles[rand()]
        retries = 20
        custom_badwords = ['reddit', 'redditor']
        profanity.load_words(custom_badwords)
        while profanity.contains_profanity(post):
            post = titles[rand()]
            retries -= 1
            if retries < 1:
                break

        return post
    except Exception as ex:
        self.logging.error(str(ex))
        return 'There is a feed problem at the moment'


def shower_thought(self):
    """ returns a (one) random shower thought """
    url = "http://www.reddit.com/r/showerthoughts/hot/.json"
    return get_random_title(self, url)


def did_you_know(self):
    """ returns a (one) random did you know """
    url = "http://www.reddit.com/r/didyouknow/hot/.json"
    text = get_random_title(self, url)
    text = text.replace('DYK', 'Did you know')
    text = text.replace('DKY', 'Did you know')
    if "Did you know" not in text:
        text = 'Did you know ' + lower_first(text)
    return text


def lower_first(s):
    """ Return string with lowercase first letter (for prefixing text to sentence) """
    if len(s) == 0:
        return s
    else:
        return s[0].lower() + s[1:]
