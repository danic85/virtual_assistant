#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser

def top_stories(numItems):

    feeds = ['http://feeds.bbci.co.uk/news/rss.xml?edition=uk', 'http://feeds.bbci.co.uk/news/technology/rss.xml?edition=uk']

    response = ''
    for feed in feeds:
        d = feedparser.parse(feed)

        cnt = 0
        for entry in d['entries']:
          if 'sport' in entry['link']:
            continue
          response += entry['summary_detail']['value'] + "\n" + entry['link']
          cnt += 1
          if cnt >= numItems:
            response += "\n\n"
            break;
          else:
            response += "\n\n"

    return response 
