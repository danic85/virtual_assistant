#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from dateutil import parser
import datetime
import inflect
from behaviours.behaviour import Behaviour

import dateparser


class Countdown(Behaviour):

    routes = {
        '^countdown ([0-9]{1,2}-[0-9]{1,2}-[0-9]{4}) ([ a-z0-9\'\"]+)': 'set_countdown',
        '^get countdowns$': 'get_all',
        '^get closest countdowns$': 'get_closest'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'countdowns'
        # self.clear_db()

    def set_countdown(self):
        """ Add countdown to countdowns list """
        date_str, description = self.match.groups()
        # date = parser.parse(date_str)
        date = dateparser.parse(date_str, date_formats=['%d-%m-%Y'])
        countdown = self.db.find_one(self.collection, {'date': date})
        if countdown is None:
            countdown = {'date': date}
        countdown['description'] = description
        self.db.upsert(self.collection, countdown)
        return self.get_all()

    def get_closest(self):
        """ Get first 2 countdowns from list """
        countdowns = self.__get_countdowns()
        return '\n'.join(countdowns[:2])

    def get_all(self):
        """ Get all countdowns from list """
        countdowns = self.__get_countdowns()
        return '\n'.join(countdowns)

    def __get_countdowns(self):
        """ Parse countdowns from db collection """
        countdowns = []
        for countdown in self.db.find(self.collection, {}, [('date', 1)]):
            delta = countdown['date'] - datetime.datetime.now()
            if delta.days > 0 or delta.days < 0:
                days = delta.days
            elif countdown['date'] > datetime.datetime.now():
                days = 1
            else:
                days = 0

            if days < 0:
                self.db.delete(countdown)  # remove old countdown
            elif days == 0:
                countdowns.append('Today is %s!' % countdown['description'])  # @todo i18n
            else:
                p = inflect.engine()
                countdowns.append('%d %s until %s' % (days, p.plural("day", days),
                                                      countdown['description']))  # @todo i18n

        if len(countdowns) < 1:
            countdowns.append("You have no countdowns active")
        return countdowns
