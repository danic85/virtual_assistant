#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from dateutil import parser
import datetime
import inflect
from behaviours.behaviour import Behaviour

import dateparser


class Reminder(Behaviour):

    routes = {
        '^Remind (?P<who>me|us) ((at (?P<time>[0-9]{1,2})|(in (?P<hours>[0-9]{1,2}) hours))|((?P<tod_context>this|tomorrow|to) ?(?P<tod_section>morning|lunch(time)?|afternoon|evening|night))) (?:that (I|we) (need|have) )?to (?P<task>.*)$': 'set_reminder',
        '^check reminders$': 'check_reminders',
        '^output reminders$': 'output_reminders',
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'reminders'
        self.define_idle('check_reminders', 0)
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
            dt = self.__get_datetime_from_time(self.match.group('time'))
        if dt is None and self.match.group('tod_context') and self.match.group('tod_section'):
            dt = self.__get_datetime_from_time_of_day()
        if dt is None and self.match.group('hours'):
            dt = self.__get_datetime_from_hours(self.match.group('hours'))

        reminders = []
        for user in self.act.user:
            reminders.append({'date': dt, 'user': int(user), 'task': self.match.group('task')})

        self.db.insert(self.collection, reminders)
        return 'Reminder set for ' + str(dt) + ' to ' + self.match.group('task')

    def __get_datetime_from_time(self, time):
        return self.get_datetime_from_time(int(time), 0)

    def __get_datetime_from_time_of_day(self):
        dt = datetime.datetime.now()
        if self.match.group('tod_context') == 'tomorrow':
            dt = dt + datetime.timedelta(days=1)

        time = 0
        if self.match.group('tod_section') == 'morning':
            time = 7

        if self.match.group('tod_section') == 'lunch' or self.match.group('tod_section') == 'lunchtime':
            time = 12

        if self.match.group('tod_section') == 'afternoon':
            time = 15

        if self.match.group('tod_section') == 'evening':
            time = 19

        if self.match.group('tod_section') == 'night':
            time = 22

        dt = datetime.datetime(dt.year, dt.month, dt.day, time, 0)

        return dt

    def __get_datetime_from_hours(self, hours):
        return datetime.datetime.now() + datetime.timedelta(hours=int(hours))

    def get_all(self):
        reminders = self.db.find(self.collection, {})
        return reminders
