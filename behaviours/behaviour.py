#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta
import re
from db import Database
from datetime import datetime, timedelta
import collections

class Behaviour(object):
    """An abstract base class to define all behaviours

    Attributes:
        act: reference to interaction object
        db: database connection
        collection: name of db collection
        match: result of regular expression search (including capture groups)
        execution_order: Order in which to execute command against behaviour (useful to command vs chat behaviour)
        history: collection of history json objects for each user

    """
    __metaclass__ = ABCMeta

    routes = collections.OrderedDict()  # this allows us to set the order of execution when needed

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
        self.history = {}

    def handle(self, act):
        self.act = act

        # @todo i18n support on regular expressions
        for theRegex in self.routes:
            self.match = re.search(theRegex, self.act.command['text'], re.IGNORECASE)
            # print('Trying: ' + theRegex)
            if self.match:
                print('Match on ' + theRegex)
                func = getattr(self, self.routes[theRegex])
                response = func()
                return response

        return None

    def idle(self, act):
        """ Anything that needs to be executed continuously during operation """
        pass

    def set_history(self, user, history):
        if 'time' not in history:
            history['time'] = datetime.now()
        self.history[int(user)] = history
        print('History added:')
        print(self.history)

    def get_recent_history(self, user):
        if int(user) not in self.history:
            print('No history found')
            return None
        recent = self.history[int(user)]
        if recent['time'] < datetime.now() - timedelta(minutes=1):
            print('Found history but expired')
            return None
        print('Found history')
        print(recent)
        return recent
