#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Powered by NewsAPI.org """

import requests

def news_api_feed(self, feeds, num_items):
    response = []
    for feed in feeds:
        r = requests.get(feed, verify=False)
        d = r.json()

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


def news_api_sources_sort(source, sources_json):
    for entry in sources_json['sources']:
        if entry['id'] == source:
            return entry['sortBysAvailable'][0]
    return 'top'


def get_news_api_sources(self):
    r = requests.get('https://newsapi.org/v1/sources?language=en', verify=False)
    return r.json()


def news_api_sources(self):
    sources_json = get_news_api_sources(self)
    print sources_json
    response = []
    for entry in sources_json['sources']:
        response.append(entry['id'] + " - " + entry['name'])

    return '\n'.join(response)


def top_stories(self):
    sources = self.config.get('Config', 'News')
    source_list = sources.split(',')

    sources_json = get_news_api_sources(self)

    num_items = 5
    feeds = []

    for s in source_list:
        feeds.append('https://newsapi.org/v1/articles?source=' + s + '&sortBy=' + news_api_sources_sort(s, sources_json) + '&apiKey=' + self.config.get('Config', 'NewsAPIKey'))

    return news_api_feed(self, feeds, num_items)

