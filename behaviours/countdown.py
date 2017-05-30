#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil import parser
import datetime
import inflect
from behaviour import Behaviour


class Countdown(Behaviour):

    routes = {
        '^countdown ([0-9]{2}-[0-9]{2}-[0-9]{4}) ([ a-z]+)': 'set_countdown',
        '^get countdowns$': 'get_all',
        '^get closest countdowns$': 'get_closest'
    }

    def __init__(self):
        super(self.__class__, self).__init__()
        self.collection = 'countdowns'

    def set_countdown(self):
        """ Add countdown to countdowns list """
        date_str, description = self.match.groups()
        date = parser.parse(date_str)
        self.db.insert(self.collection, {'date': date, 'description': description})
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
            days = (countdown['date'] - datetime.datetime.now()).days + 1
            if days < 0:
                self.db.delete(countdown)  # remove old countdown
            elif days == 0:
                countdowns.append('Today is %s!' % countdown['description'])  # @todo i18n
            else:
                p = inflect.engine()
                countdowns.append('%d %s until %s' % (days, p.plural("day", days),
                                                      countdown['description']))  # @todo i18n
        return countdowns
