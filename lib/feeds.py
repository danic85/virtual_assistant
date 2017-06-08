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


def get_json(endpoint, params=None, headers=None):
    """ Returns json object from request url """
    if params:
        endpoint = endpoint + '?' + '&'.join(params)
    if headers:
        opener = build_opener()
        opener.addheaders = headers
        data = opener.open(endpoint).read().decode('utf8')
        return json.loads(data)
    else:
        return requests.get(endpoint, verify=False).json()


def get_rss(endpoint):
    return feedparser.parse(endpoint)