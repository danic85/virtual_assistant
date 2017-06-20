#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import re
from random import randint
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

        # routes set here due to use OrderedDict
        self.routes['train echochat'] = 'train'
        self.routes['(.*)'] = 'chat'

        self.define_idle(self.train, randint(2, 36))

    def chat(self):
        previous_id = self.__log_new_response()

        for stuff in self.db.find(self.collection, {}):
            self.logging.info(stuff)
            # self.db.delete(stuff)

        match = self.db.find(self.collection, {'msg': self.act.command['text'], 'previous_id': previous_id})
        self.logging.info('FOUND:')
        self.logging.info(match.count())
        for r in match:
            id = r.get('_id')
            results = self.db.find(self.collection, {'previous_id': id})
            if results.count() > 0:
                self.set_history(self.act.user[0], results[0])
                return results[0].get('msg')

        # If not found repeat message to user for training
        return "I'm sorry I don't know what to say. How would you respond to that?"

    def __log_new_response(self):
        previous_id = None
        usr = int(self.act.user[0])

        self.logging.info(usr)

        history = self.get_recent_history(usr)
        if history:
            previous_id = history.get('_id')

        self.logging.info(previous_id)
        exists = self.db.find(self.collection, {'msg': re.compile(self.match.group(0), re.IGNORECASE),
                                                'previous_id': previous_id})
        if exists.count() == 0:
            self.logging.info('does not exist')
            new_response = {'msg': self.match.group(0), 'previous_id': previous_id}
            new_response['id'] = self.db.insert(self.collection, new_response)
            self.set_history(usr, new_response)
        else:
            self.logging.info('already exists')
        return previous_id

    def train(self):
        response = self.db.find_random(self.collection, {'previous_id': None})
        if response is not None:
            return response.get('msg')

        return "I don't have anything to say yet, teach me something!"
