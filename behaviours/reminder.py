#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from dateutil import parser
import datetime
import inflect
from behaviours.behaviour import Behaviour
import lib.dt

import dateparser


class Reminder(Behaviour):

    routes = {
        '^Remind (?P<who>me|us) ((at (?P<time>[0-9]{1,2})|(in (?P<hours>[0-9]{1,2}) hours))|((?P<which_day>this|tomorrow|to) ?(?P<which_period>morning|lunch(time)?|afternoon|evening|night))) (?:that (I|we) (need|have) )?to (?P<task>.*)$': 'set_reminder',
        '^check reminders$': 'check_reminders',
        '^output reminders$': 'output_reminders',
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'reminders'
        self.define_idle(self.check_reminders, 0)
        # self.clear_db()

    def output_reminders(self):
        reminders = self.get_all()
        for r in reminders:
            self.act.respond(str(r))
        return None

    def check_reminders(self):
        """ Check all reminders and if there are any due message the user and delete the reminder """
        reminders = self.get_all()
        action = []
        for r in reminders:
            if r['date'] <= datetime.datetime.now():
                action.append(r)

        if len(action) > 0:
            for r in action:
                self.act.respond('Remember to ' + r['task'], r['user'])  # @todo send to the right person!
                self.db.delete(r)

        return None

    def set_reminder(self):
        """ Add reminder based on natural language """

        if self.match.group('who') == 'us':
            self.act.user = self.config.get('users').split(',')

        dt = None
        if self.match.group('time'):
            dt = lib.dt.datetime_from_time(int(self.match.group('time')), 0)
        if dt is None and self.match.group('which_day') and self.match.group('which_period'):
            dt = lib.dt.datetime_from_time_of_day(self.match.group('which_day'), self.match.group('which_period'))
        if dt is None and self.match.group('hours'):
            dt = lib.dt.datetime_from_hours(self.match.group('hours'))

        reminders = []
        for user in self.act.user:
            reminders.append({'date': dt, 'user': int(user), 'task': self.match.group('task')})

        self.db.insert(self.collection, reminders)
        return 'Reminder set for ' + str(dt) + ' to ' + self.match.group('task')

    def get_all(self):
        reminders = self.db.find(self.collection, {})
        return reminders
