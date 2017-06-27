import unittest
from mock import Mock, call, patch
import datetime
from lib.interaction import Interaction
from behaviours import reminder
import re
from freezegun import freeze_time


class TestReminderMethods(unittest.TestCase):

    def test_routes(self):
        b = reminder.Reminder(db=None, config={}, dir='')
        act = Interaction(user=[1234])

        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        b.set_reminder = Mock()
        b.get_all = Mock()

        response = b.handle(act)
        self.assertEqual(response, None)

        b.set_reminder = Mock()
        act.command = {'text': 'remind me at 7 to do something'}
        b.handle(act)
        b.set_reminder.assert_called_once()
        self.assertEqual(b.match.group('time'), '7')
        self.assertEqual(b.match.group('tod_section'), None)
        self.assertEqual(b.match.group('tod_context'), None)
        self.assertEqual(b.match.group('task'), 'do something')

        b.set_reminder = Mock()
        act.command = {'text': 'remind me in 3 hours to do something'}
        b.handle(act)
        b.set_reminder.assert_called_once()
        self.assertEqual(b.match.group('time'), None)
        self.assertEqual(b.match.group('hours'), '3')
        self.assertEqual(b.match.group('tod_section'), None)
        self.assertEqual(b.match.group('tod_context'), None)
        self.assertEqual(b.match.group('task'), 'do something')

        b.set_reminder = Mock()
        act.command = {'text': 'remind me tomorrow night to do something'}
        b.handle(act)
        b.set_reminder.assert_called_once()
        self.assertEqual(b.match.group('time'), None)
        self.assertEqual(b.match.group('tod_section'), 'night')
        self.assertEqual(b.match.group('tod_context'), 'tomorrow')
        self.assertEqual(b.match.group('task'), 'do something')

        b.set_reminder = Mock()
        act.command = {'text': 'remind me this morning to do something'}
        b.handle(act)
        b.set_reminder.assert_called_once()
        self.assertEqual(b.match.group('time'), None)
        self.assertEqual(b.match.group('tod_section'), 'morning')
        self.assertEqual(b.match.group('tod_context'), 'this')
        self.assertEqual(b.match.group('task'), 'do something')

        b.set_reminder = Mock()
        act.command = {'text': 'remind me tomorrow morning that I have to do something'}
        b.handle(act)
        b.set_reminder.assert_called_once()
        self.assertEqual(b.match.group('time'), None)
        self.assertEqual(b.match.group('tod_section'), 'morning')
        self.assertEqual(b.match.group('tod_context'), 'tomorrow')
        self.assertEqual(b.match.group('task'), 'do something')

    @freeze_time("2017-01-01 11:00")
    def test_get_all(self):
        b = reminder.Reminder(db=None, config={'users': "1234,12345"}, dir='')
        b.act = Interaction(user=[1234])
        b.db = Mock()
        b.db.delete = Mock()
        test_data = [{'date': datetime.datetime(2017, 1, 2, 22, 0),
                                                      'task': 'do something', 'user': 1234},{'date': datetime.datetime(2017, 1, 2, 22, 0),
                                                      'task': 'do something', 'user': 12345}]
        b.db.find = Mock(return_value=test_data)

        self.assertEqual(b.get_all(), test_data)
        b.db.find.assert_called_with({})

    @freeze_time("2017-01-01 11:00")
    def test_set_reminder(self):
        b = reminder.Reminder(db=None, config={'users': "1234,12345"}, dir='')
        b.act = Interaction(user=[1234])
        b.db = Mock()
        b.db.delete = Mock()
        b.db.insert = Mock()

        regex = '^Remind (?P<who>me|us) ((at (?P<time>[0-9]{1,2})|(in (?P<hours>[0-9]{1,2}) hours))|((?P<tod_context>this|tomorrow|to) ?(?P<tod_section>morning|lunch(time)?|afternoon|evening|night))) (?:that (I|we) (need|have) )?to (?P<task>.*)$'

        # test time setting, should increment day if after current time
        b.match = re.search(regex,
                            'remind me at 7 to do something', re.IGNORECASE)

        self.assertEqual(b.set_reminder(), "Reminder set for 2017-01-02 07:00:00 to do something")
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 2, 7, 0),
                                                      'task': 'do something', 'user': 1234}])
        b.db.delete.assert_not_called()

        # test hour setting
        b.db.insert = Mock()
        b.match = re.search(regex,
            'remind me in 3 hours to do something', re.IGNORECASE)
        self.assertEqual(b.set_reminder(), "Reminder set for 2017-01-01 14:00:00 to do something")
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 1, 14, 0),
                                                     'task': 'do something', 'user': 1234}])
        b.db.delete.assert_not_called()

        # test time of day setting
        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me this morning to do something', re.IGNORECASE)
        self.assertEqual(b.set_reminder(), "Reminder set for 2017-01-01 07:00:00 to do something")
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 1, 7, 0),
                                                     'task': 'do something', 'user': 1234}])
        b.db.delete.assert_not_called()

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me this lunchtime to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 1, 12, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me this afternoon to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 1, 15, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me this evening to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 1, 19, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me tonight to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 1, 22, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.match = re.search(regex,
                            'remind me tomorrow morning to do something', re.IGNORECASE)
        self.assertEqual(b.set_reminder(), "Reminder set for 2017-01-02 07:00:00 to do something")
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 2, 7, 0),
                                                     'task': 'do something', 'user': 1234}])
        b.db.delete.assert_not_called()

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me tomorrow lunchtime to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 2, 12, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me tomorrow afternoon to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 2, 15, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me tomorrow evening to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 2, 19, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind me tomorrow night to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 2, 22, 0),
                                                     'task': 'do something', 'user': 1234}])

        b.db.insert = Mock()
        b.match = re.search(regex,
                            'remind us tomorrow night to do something', re.IGNORECASE)
        b.set_reminder()
        b.db.insert.assert_called_with('reminders', [{'date': datetime.datetime(2017, 1, 2, 22, 0),
                                                      'task': 'do something', 'user': 1234},{'date': datetime.datetime(2017, 1, 2, 22, 0),
                                                      'task': 'do something', 'user': 12345}])
