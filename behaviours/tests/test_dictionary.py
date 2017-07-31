import unittest
from mock import Mock, call, patch
from lib import feeds
from behaviours import dictionary
from lib.interaction import Interaction


class TestDictionaryMethods(unittest.TestCase):

    def test_routes(self):
        b = dictionary.Dictionary(db=None, config={}, dir='')
        act = Interaction()
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)
        b.word_of_the_day = Mock()

        response = b.handle(act)
        self.assertEqual(response, None)
        act.command = {'text': 'word of the day'}
        b.handle(act)
        b.word_of_the_day.assert_called_once()

    def test_word_of_the_day(self):
        feeds.get_rss = Mock()
        feeds.get_rss.side_effect = [{'entries': [{'summary_detail': {'value': 'Test word'}}]}]

        b = dictionary.Dictionary(db=None, config={}, dir='')
        self.assertEqual(b.word_of_the_day(), "The word of the day is Test word")
