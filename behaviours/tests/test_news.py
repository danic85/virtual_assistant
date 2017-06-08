import datetime, unittest
import os, sys
from mock import Mock, call, patch
from freezegun import freeze_time
from lib import feeds
import json
from behaviours import news


class TestNewsMethods(unittest.TestCase):

    @freeze_time("2017-06-07")
    def test_news_sources(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/news_news_sources.json'
        with open(path) as data_file:
            data = json.load(data_file)

        feeds.get_json = Mock(return_value=data)
        g = news.News(db=None, config={}, dir='')
        self.assertEqual(g.news_sources()[0:30], "abc-news-au - ABC News (AU)\nal")

    @freeze_time("2017-06-07")
    def test_top_stories(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/news_top_stories.json'
        with open(path) as data_file:
            data = json.load(data_file)

        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/news_news_sources.json'
        with open(path) as data_file:
            sources = json.load(data_file)

        feeds.get_json = Mock()
        feeds.get_json.side_effect = [sources, data]
        config = Mock()
        config.get = Mock(return_value='independent')
        g = news.News(db=None, config=config, dir='')
        self.assertEqual(g.top_stories()[0:30], "Election 2017 live updates: Th")

    @freeze_time("2017-06-07")
    def test_top_stories_default_sort(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/news_top_stories.json'
        with open(path) as data_file:
            data = json.load(data_file)

        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/news_news_sources.json'
        with open(path) as data_file:
            sources = json.load(data_file)

        feeds.get_json = Mock()
        feeds.get_json.side_effect = [sources, data]
        config = Mock()
        config.get = Mock(return_value='nomatch')
        g = news.News(db=None, config=config, dir='')
        self.assertEqual(g.top_stories()[0:30], "Election 2017 live updates: Th")

    @freeze_time("2017-06-07")
    def test_top_stories_error(self):

        data = {'status': 'error', 'message': 'error!'}
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/news_news_sources.json'
        with open(path) as data_file:
            sources = json.load(data_file)

        feeds.get_json = Mock()
        feeds.get_json.side_effect = [sources, data]
        config = Mock()
        config.get = Mock(return_value='independent')
        g = news.News(db=None, config=config, dir='')
        self.assertEqual(g.top_stories()[0:6], "error!")
