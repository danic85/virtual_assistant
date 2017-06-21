#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import re
from abc import ABCMeta
from datetime import datetime, timedelta

from lib.db import Database
from bson.json_util import dumps

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
        self.idle_methods = []
        self.define_idle(self.export_db, 24, self.get_datetime_from_time(0, 0))  # export db nightly

    def handle(self, act):
        self.act = act

        # @todo i18n support on regular expressions
        for theRegex in self.routes:
            self.match = re.search(theRegex, self.act.command['text'], re.IGNORECASE)
            # self.logging.info('Trying: ' + theRegex)
            if self.match:
                self.logging.info('Match on ' + theRegex)
                func = getattr(self, self.routes[theRegex])
                response = func()
                return response

        return None

    def idle(self, act):
        """ Anything that needs to be executed continuously during operation """
        self.act = act
        for method in self.idle_methods:
            if datetime.now() > method['next']:
                method['next'] = datetime.now() + timedelta(hours=method['interval'])
                self.act.respond(method['method']())
        return None

    @staticmethod
    def get_datetime_from_time(hour, minute):
        dt = datetime.now()
        if dt.hour > hour and dt.minute > minute:  # don't fire straight away, make it for tomorrow if earlier than now
            dt = datetime.now() + timedelta(days=1)
        return datetime(dt.year, dt.month, dt.day, hour, minute, 0)

    def define_idle(self, method, interval, first=None):
        if first is None:
            first = datetime.now() + timedelta(hours=interval)
        self.idle_methods.append(
            {'method': method,
             'interval': interval,
             'next': first
            })

    def set_history(self, user, history):
        if 'time' not in history:
            history['time'] = datetime.now()
        self.history[int(user)] = history
        self.logging.info('History added:')
        self.logging.info(self.history)

    def get_recent_history(self, user):
        if int(user) not in self.history:
            self.logging.info('No history found')
            return None
        recent = self.history[int(user)]
        if recent['time'] < datetime.now() - timedelta(minutes=1):
            self.logging.info('Found history but expired')
            return None
        self.logging.info('Found history')
        self.logging.info(recent)
        return recent

    def export_db(self):
        """ Export of database collection to json file """
        if self.collection:
            response = self.db.find(self.collection, {})
            with open(self.files + '/db_exports/'+self.collection+'.txt', 'w') as outfile:
                outfile.write(dumps(response))

    def clear_db(self):
        """ Call this from any behaviour to clear the given collection """
        if self.collection:
            print('*** Clearing db collection: '+ self.collection)
            response = self.db.find(self.collection, {})
            for r in response:
                self.db.delete(r)
