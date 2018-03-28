#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pyowm
from lib import feeds
from datetime import datetime
import calendar
from behaviours.behaviour import Behaviour
import json
import re


class Translator(Behaviour):

    """
        Unfortunately this doesn't work because the API provider is no longer active.
    """

    routes = {
        '^translate (.*) (to|from) (\w*)$': 'translate'
    }

    endpoints = {
        'translate': 'http://www.transltr.org/api/translate',
        'languages': 'http://www.transltr.org/api/getlanguagesfortranslate'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.languages = None

    def translate(self):
        params = ['text=' + self.match.group(1)]

        language = self.__get_language_code(self.match.group(3))

        if language is None:
            return "I can't translate " + self.match.group(2) + " " + self.match.group(3)

        if 'from' in self.match.group(2):
            params.append('from=' + language)
            params.append('to=en')
        else:
            params.append('to=' + language)
            params.append('from=en')
        r = feeds.get_json(self.endpoints['translate'], params)
        if r is None:
            return 'There was a problem with the translator'
        return r['translationText']

    def __get_language_code(self, language):
        if self.languages is None:
            self.languages = feeds.get_json(self.endpoints['languages'])
        if self.languages:
            for r in self.languages:
                if re.search(r['languageName'], language, re.IGNORECASE):
                    return r['languageCode']
        return None
