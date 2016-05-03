#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser

def top_stories(numItems):

    feed = 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk'

    d = feedparser.parse(feed)
    
    intro = 'Top Stories:'

    response = ''
    cnt = 0
    for entry in d['entries']:
      if 'sport' in entry['link']:
        continue
      response += entry['summary_detail']['value'] + "\n" + entry['link']
      cnt += 1
      if cnt >= numItems:
        break;
      else:
        response += "\n\n"

    return response 
