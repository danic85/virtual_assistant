#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta
import re
from db import Database


class Behaviour(object):
    """An abstract base class to define all behaviours

    Attributes:
        bot: reference to bot object
        db: database connection
        collection: name of db collection
        match: result of regular expression search (including capture groups)

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.bot = {}
        self.db = Database()
        self.collection = ''
        self.match = None

    def handle(self, bot):
        self.bot = bot

        # @todo i18n support on regular expressions
        for theRegex in self.routes:
            self.match = re.search(theRegex, self.bot.original_message, re.IGNORECASE)
            if self.match:
                print('Match on ' + theRegex)
                func = getattr(self, self.routes[theRegex])
                return func()

        return None
