#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behaviours.behaviour import Behaviour
from lib import feeds


class Dictionary(Behaviour):

    routes = {
        'word of the day': 'word_of_the_day'
    }

    endpoints = {
        'wotd': 'http://www.dictionary.com/wordoftheday/wotd.rss'
    }

    def word_of_the_day(self):
        d = feeds.get_rss(self.endpoints['wotd'])
        return 'The word of the day is ' + d['entries'][0]['summary_detail']['value']
