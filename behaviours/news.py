#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Powered by NewsAPI.org """

from lib import feeds
from behaviours.behaviour import Behaviour
import json

class News(Behaviour):

    routes = {
        '^news sources$': 'news_sources',
        '^news$': 'top_stories'
    }

    endpoints = {
        'articles': 'https://newsapi.org/v1/articles',
        'sources': 'https://newsapi.org/v1/sources'
    }

    def news_sources(self):
        sources_json = self.__get_sources()
        response = []
        for entry in sources_json['sources']:
            response.append(entry['id'] + " - " + entry['name'])

        return '\n'.join(response)

    def top_stories(self):
        sources = self.config.get('Config', 'News')  # @todo Make user specific
        source_list = sources.split(',')

        sources_json = self.__get_sources()

        num_items = 5
        feeds = []

        for s in source_list:
            feeds.append(self.endpoints['articles'] + '?source=' + s +
                         '&sortBy=' + self.__sort_sources(s, sources_json) +
                         '&apiKey=' + self.config.get('Config', 'NewsAPIKey'))

        return self.__parse_feed(feeds, num_items)

    @staticmethod
    def __parse_feed(feed_list, num_items):
        response = []
        for feed in feed_list:
            d = feeds.get_json(feed, None, None, False)
            if d['status'] == 'error':
                response.append(d['message'] + '\n' + feed)
                continue

            cnt = 0
            for entry in d['articles']:
                response.append(entry['title'] + "\n" + entry['url'])
                cnt += 1
                if cnt >= num_items:
                    break

        return '\n\n'.join(response)

    def __get_sources(self):
        params = {'language=en'}
        return feeds.get_json(self.endpoints['sources'], params, None, False)  # @todo make language user specific

    @staticmethod
    def __sort_sources(source, sources_json):
        for entry in sources_json['sources']:
            if entry['id'] == source:
                return entry['sortBysAvailable'][0]
        return 'top'




