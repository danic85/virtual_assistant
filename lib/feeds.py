#!/usr/bin/python
# -*- coding: latin-1 -*-
# Source: https://github.com/xDHILEx/Shower-Thoughts/blob/master/Reddit.py

import json
import sys
import requests
import feedparser

if sys.version_info < (3, 0):
    from urllib2 import build_opener
else:
    from urllib.request import build_opener


def get_json(endpoint, params=None, headers=None, secure=True):
    """ Returns json object from request url """
    if params:
        endpoint = endpoint + '?' + '&'.join(params)
    if headers:
        opener = build_opener()
        opener.addheaders = headers
        data = opener.open(endpoint).read().decode('utf8')
        return json.loads(data)
    else:
        response = requests.get(endpoint, verify=secure)
        if response.status_code != 200:
            return None
        return response.json()

def post_json(endpoint, params=None):
    """ Returns json object from post request url """
    return requests.post(endpoint, data=params).json()

def get_rss(endpoint):
    return feedparser.parse(endpoint)