import datetime, unittest
import os, sys
from mock import Mock, call, patch
from freezegun import freeze_time
from lib import feeds
import json
from behaviours import weather


class TestWeatherMethods(unittest.TestCase):

    @freeze_time("2017-06-07")
    def test_forecast(self):
        # output to console via print(json.dumps(forecast)) in weather.forecast()
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/weather_forecast.json'
        with open(path) as data_file:
            data = json.load(data_file)

        feeds.get_json = Mock(return_value=data)
        g = weather.Weather(db=None, config={}, dir='')
        g.config = Mock()
        g.config.get = Mock(return_value='value')
        self.assertEqual(g.forecast(), "It is likely to rain on Monday, Wednesday, Thursday, Friday, Saturday and Sunday\nIt is likely to be icy on Wednesday")