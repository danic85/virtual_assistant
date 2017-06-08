import unittest
from mock import Mock, call, patch
import datetime
from lib.interaction import Interaction
from behaviours import countdown
import re
from freezegun import freeze_time

class TestCountdownMethods(unittest.TestCase):

    def test_routes(self):
        b = countdown.Countdown(db=None, config={}, dir='')
        act = Interaction()
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        b.set_countdown = Mock()
        b.get_closest = Mock()
        b.get_all = Mock()

        response = b.handle(act)
        self.assertEqual(response, None)

        act.command = {'text': 'get countdowns'}
        b.handle(act)
        b.get_all.assert_called_once()

        act.command = {'text': 'get closest countdowns'}
        b.handle(act)
        b.get_closest.assert_called_once()

        act.command = {'text': 'countdown 12-05-2015 my countdown message'}
        b.handle(act)
        b.set_countdown.assert_called_once()
        self.assertEqual(b.match.group(1), '12-05-2015')
        self.assertEqual(b.match.group(2), 'my countdown message')

    @freeze_time("2017-01-01")
    def test_get_all_none(self):
        b = countdown.Countdown(db=None, config={}, dir='')
        b.db = Mock()
        b.db.find = Mock(return_value=[])
        self.assertEqual(b.get_all(), 'You have no countdowns active')
        b.db.delete.assert_not_called()

    @freeze_time("2017-01-01")
    def test_get_all(self):
        b = countdown.Countdown(db=None, config={}, dir='')
        b.db = Mock()
        b.db.find = Mock(return_value=[
                {'date': datetime.datetime.now(), 'description': 'my today countdown'},
                {'date': datetime.datetime.now() + datetime.timedelta(days=1), 'description': 'my tomorrow countdown'},
                {'date': datetime.datetime.now() + datetime.timedelta(days=10), 'description': 'my next countdown'}
            ])
        self.assertEqual(b.get_all(), 'Today is my today countdown!\n1 day until my tomorrow countdown\n10 days until my next countdown')
        b.db.delete.assert_not_called()

    @freeze_time("2017-01-01")
    def test_get_closest(self):
        b = countdown.Countdown(db=None, config={}, dir='')
        b.db = Mock()
        b.db.delete = Mock()
        b.db.find = Mock(return_value=[
                {'date': datetime.datetime.now() + datetime.timedelta(days=10), 'description': 'my countdown'},
                {'date': datetime.datetime.now() + datetime.timedelta(days=10), 'description': 'my countdown'},
                {'date': datetime.datetime.now() + datetime.timedelta(days=10), 'description': 'my countdown'}
            ])
        self.assertEqual(b.get_closest(), '10 days until my countdown\n10 days until my countdown')
        b.db.delete.assert_not_called()

    @freeze_time("2017-01-01")
    def test_remove_old_countdowns(self):
        b = countdown.Countdown(db=None, config={}, dir='')
        b.db = Mock()
        b.db.delete = Mock()
        b.db.find = Mock(return_value=[
                {'date': datetime.datetime.now() + datetime.timedelta(days=-1), 'description': 'my tomorrow countdown'},
            ])
        b.get_closest()
        b.db.delete.assert_called_once()

    @freeze_time("2017-01-01")
    def test_set_countdown(self):
        b = countdown.Countdown(db=None, config={}, dir='')
        b.db = Mock()
        b.db.delete = Mock()
        b.db.insert = Mock()

        key, value = next(iter(b.routes.items()))

        b.match = re.search(key, 'countdown 02-01-2017 my countdown message', re.IGNORECASE)

        b.db.find = Mock(return_value=[
            {'date': datetime.datetime(2017, 1, 2, 0, 0), 'description': 'my countdown message'},
        ])

        assert datetime.datetime.now() == datetime.datetime(2017, 1, 1)

        self.assertEqual(b.set_countdown(), '1 day until my countdown message')
        b.db.insert.assert_called_with('countdowns', {'date': datetime.datetime(2017, 1, 2, 0, 0), 'description': 'my countdown message'})
        b.db.delete.assert_not_called()
