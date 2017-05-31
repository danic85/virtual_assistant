#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import re
from behaviours.behaviour import Behaviour


class Echochat(Behaviour):

    """ Learning chatbot behaviour.

        Teach it conversations by responding to messages it sends within 1 minute.
        Training is initiated periodically
        """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'echochat'
        self.execution_order = 10  # execute after all other commands
        self.interval = 16
        self.__set_training_interval(self.interval)

        # routes set here due to use OrderedDict
        self.routes['train echochat'] = 'train'
        self.routes['(.*)'] = 'chat'

    def idle(self):
        if datetime.now() < self.train_time:
            self.__set_training_interval(self.interval)
            self.train()

    def __set_training_interval(self, interval):
        self.train_time = datetime.now() + timedelta(hours=interval)

    def chat(self):
        self.__log_new_response()

        for stuff in self.db.find(self.collection, {}):
            print(stuff)
            # self.db.delete(stuff)

        match = self.db.find(self.collection, {'msg': self.act.command['text']})
        for r in match:
            id = r.get('_id')
            results = self.db.find(self.collection, {'previous_id': id})
            if results.count() > 0:
                return results[0].get('msg')



        return "I don't know what to say to that... How would you respond?"

    def __log_new_response(self):
        previous_id = None
        usr = int(self.act.user[0])
        # self.last_response[usr] = {'msg': 'hello Mojo', 'time': datetime.now()}
        # print(self.last_response)
        # print(self.last_response[usr])
        # print(usr in self.last_response)
        if usr in self.last_response:
            # print('found last response')
            expired = self.last_response[usr]['time'] < datetime.now() - timedelta(minutes=1)
            if not expired:
                # print('not expired')
                results = self.db.find(self.collection, {'msg': self.last_response[usr]['msg']})
                for r in results:
                    # print('found previous id')
                    previous_id = r.get('_id')

        exists = self.db.find(self.collection, {'msg': re.compile(self.match.group(0), re.IGNORECASE), 'previous_id': previous_id})
        if exists.count() == 0:
            self.db.insert(self.collection, {'msg': self.match.group(0), 'previous_id': previous_id})

    def train(self):
        response = self.db.find_random(self.collection, {'previous_id': None})
        if response is not None:
            return response.get('msg')

        return "I don't have anything to say yet, teach me something!"
