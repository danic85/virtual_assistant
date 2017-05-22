#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime


def set_countdown(self):
    """ Add countdown to countdowns list """
    cmd = self.command.replace('countdown ', '')
    with open(self.files + '/countdowns.txt', 'a') as f:
        f.write(cmd + '\n')
    return get_all(self)


def get_closest(self):
    """ Get first 2 countdowns from list """
    countdowns = read(self)
    return '\n'.join(countdowns[:2])


def get_all(self):
    """ Get all countdowns from list """
    countdowns = read(self)
    return '\n'.join(countdowns)


def read(self):
    countdowns = []
    with open(self.files + '/countdowns.txt', 'r') as f:
        for line in f:
            cmd = line.strip().split(' ', 1)
            date = cmd[0].split('-')
            event = cmd[1]
            c = countdown(self, int(date[2]), int(date[1]), int(date[0]), event)
            if c != '':
                countdowns.append(c)  # only add future events @todo remove old events from file
    return countdowns


def countdown(self, year, month, day, event):
    """ Return string of countdown """
    delta = datetime.datetime(year, month, day) - datetime.datetime.now()
    days = delta.days + 1
    if days < 0:
        return ''
    if days == 0:
        return 'Today is ' + event + '!'
    return str(days) + ' days until ' + event
