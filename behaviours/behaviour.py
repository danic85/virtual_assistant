#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta
import re
from db import Database


class Behaviour(object):
    """An abstract base class to define all behaviours

    Attributes:
        act: reference to interaction object
        db: database connection
        collection: name of db collection
        match: result of regular expression search (including capture groups)
        execution_order: Order in which to execute command against behaviour (useful to command vs chat behaviour)

    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.act = {}
        self.db = kwargs.get('db', Database())
        self.dir = kwargs.get('dir', None)
        self.files = self.dir + '/files'
        self.config = kwargs.get('config', None)
        self.collection = ''
        self.match = None
        self.execution_order = 1
        self.logging = kwargs.get('logging', None)

    def handle(self, act):
        self.act = act

        # @todo i18n support on regular expressions
        for theRegex in self.routes:
            self.match = re.search(theRegex, self.act.command['text'], re.IGNORECASE)
            if self.match:
                print('Match on ' + theRegex)
                func = getattr(self, self.routes[theRegex])
                return func()

        return None

    def idle(self):
        """ Anything that needs to be executed continuously during operation """
        pass