#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from behaviours.behaviour import Behaviour


class Dictionary(Behaviour):

    routes = {
        'word of the day': 'word_of_the_day'
    }

    endpoints = {
        'wotd': 'http://www.dictionary.com/wordoftheday/wotd.rss'
    }

    def word_of_the_day(self):
        d = feedparser.parse(self.endpoints['wotd'])
        intro = 'The word of the day is '
        return intro + d['entries'][0]['summary_detail']['value']
