import datetime, unittest
import os, sys
from mock import Mock, call, patch
from freezegun import freeze_time
from lib import feeds
import json
from behaviours import reddit


class TestRedditMethods(unittest.TestCase):

    @freeze_time("2017-06-07")
    def test_sources(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/reddit_shower_thought.json'
        with open(path) as data_file:
            data = json.load(data_file)

        with patch('behaviours.reddit.randint', return_value=3) as mock_random:
            feeds.get_json = Mock(return_value=data)
            g = reddit.Reddit(db=None, config={}, dir='')
            self.assertEqual(g.shower_thought(),
                             "As a loyal customer, I feel really ripped off when companies have a promotion for new customers but offer nothing for customers who have been with them for years.")

    @freeze_time("2017-06-07")
    def test_did_you_know(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/reddit_did_you_know.json'
        with open(path) as data_file:
            data = json.load(data_file)

        with patch('behaviours.reddit.randint', return_value=0) as mock_random:
            feeds.get_json = Mock(return_value=data)
            g = reddit.Reddit(db=None, config={}, dir='')
            self.assertEqual(g.did_you_know(),
                             "Did you know wikipedia is NOT a source. Link to the source cited by Wikipedia. reddit")

    @freeze_time("2017-06-07")
    def test_did_you_know_exception(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/reddit_did_you_know.json'
        with open(path) as data_file:
            data = json.load(data_file)

        with patch('behaviours.reddit.randint', return_value=0) as mock_random:
            feeds.get_json = Mock(return_value=data)
            feeds.get_json.side_effect = Exception()
            g = reddit.Reddit(db=None, config={}, dir='')
            self.assertEqual(g.did_you_know(),
                             "Did you know there is a feed problem at the moment: ")