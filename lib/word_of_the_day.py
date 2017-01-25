#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser


def get(self):
    feed = 'http://www.dictionary.com/wordoftheday/wotd.rss'
    d = feedparser.parse(feed)
    intro = 'The word of the day is '
    return intro + d['entries'][0]['summary_detail']['value']
