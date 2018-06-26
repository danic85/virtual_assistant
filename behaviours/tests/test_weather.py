import datetime, unittest
import os, sys
from mock import Mock, call, patch
from freezegun import freeze_time
from lib import feeds
import json
from behaviours import weather
import re

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

    # @freeze_time("2017-06-07 19:00")
    # def test_advanced_forecast(self):
    #     # output to console via print(json.dumps(forecast)) in weather.forecast()
    #     path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/weather_forecast.json'
    #     with open(path) as data_file:
    #         data = json.load(data_file)
    #
    #     feeds.get_json = Mock(return_value=data)
    #     b = weather.Weather(db=None, config={}, dir='')
    #     b.config = Mock()
    #     b.config.get = Mock(return_value='value')
    #     response = b.advanced_forecast()
    #     print(response)
    #     self.assertEqual(response,
    #                      "There will be scattered clouds until this evening, light rain until tonight, moderate rain until Thursday afternoon and then light rain until Thursday evening")
    #
    #     # check regex changes number of days to forecast
    #     regex = 'detailed (weather )?forecast( for the next (?P<days_to_forecast>[0-9]) days)?'
    #     b.match = re.search(regex,
    #                         'detailed forecast for the next 4 days', re.IGNORECASE)
    #     response = b.advanced_forecast()
    #     print(response)
    #     self.assertEqual(response,
    #                      "There will be scattered clouds until this evening, light rain until tonight, moderate rain until Thursday afternoon, light rain until Thursday evening, overcast clouds until Saturday early morning, light rain until Saturday midday and then scattered clouds until Sunday midday")