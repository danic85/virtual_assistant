#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behaviours.behaviour import Behaviour
from datetime import date


class Taketurns(Behaviour):

    routes = {
        "who's (night|turn) is it": 'turn'
    }

    def turn(self):
        # if it is monday or an odd number of days since the given date
        if date.today().weekday() != 0:
            d0 = date(2017, 1, 1)
            delta = date.today() - d0
            if delta.days % 2 == 0:
                return 'It is not your ' + self.match.group(1) + ' tonight'
        return 'It is your ' + self.match.group(1) + ' tonight'
