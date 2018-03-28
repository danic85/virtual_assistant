#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pyowm
from lib import feeds
import lib.dt
import calendar
from behaviours.behaviour import Behaviour
import json


class Weather(Behaviour):

    routes = {
        'weather forecast': 'forecast',
        'detailed (weather )?forecast( for the next (?P<days_to_forecast>[0-9]) days)?': 'advanced_forecast',
        'weather$': 'get'
    }

    endpoints = {
        'forecast': 'http://api.openweathermap.org/data/2.5/forecast'
    }

    def get(self):
        owm = pyowm.OWM(self.config.get('OpenWeatherMapKey'))

        try:
            observation = owm.weather_at_id(2655315)
            w = observation.get_weather()
            l = observation.get_location()
            return ('Weather in ' + l.get_name() + ': ' + w.get_detailed_status() + '. ' + format(
                w.get_temperature('celsius')['temp'], '.1f') + 'degrees')
        except Exception as e:
            self.logging.error(str(e))
            return "I can't check the weather at the moment"

    def forecast(self):
        args = [
            'appid=' + self.config.get('OpenWeatherMapKey'),
            'id=2642182',
            'units=metric'
        ]
        forecast = feeds.get_json(self.endpoints['forecast']+'?' + '&'.join(args))

        occurrences = {'rain': set(), 'ice': set()}

        for f in forecast['list']:
            if f['main']['temp'] < 1:
                occurrences['ice'].add(datetime.datetime.fromtimestamp(f['dt']).weekday())

            for w in f['weather']:
                if 'Rain' in w['main']:
                    occurrences['rain'].add(datetime.datetime.fromtimestamp(f['dt']).weekday())

        response = []

        if len(occurrences['rain']) > 0:
            r = []
            for o in occurrences['rain']:
                r.append(calendar.day_name[o])
            # build natural speech list of days
            response.append('It is likely to rain on ' + ' and'.join(', '.join(r).rsplit(',', 1)))

        if len(occurrences['ice']) > 0:
            r = []
            for o in occurrences['ice']:
                r.append(calendar.day_name[o])
            # build natural speech list of days
            response.append('It is likely to be icy on ' + ' and'.join(', '.join(r).rsplit(',', 1)))

        if len(response) == 0:
            response.append('No rain or ice forecast for the next 5 days')

        return '\n'.join(response)

    def advanced_forecast(self):
        print(self.match)
        if self.match and self.match.group('days_to_forecast') and int(self.match.group('days_to_forecast')) <= 5:
            days_to_forecast = int(self.match.group('days_to_forecast'))
        else:
            days_to_forecast = 2
        args = [
            'appid=' + self.config.get('OpenWeatherMapKey'),
            'id=2642182',
            'units=metric'
        ]
        forecast = feeds.get_json(self.endpoints['forecast'] + '?' + '&'.join(args))
        changes = []

        for f in forecast['list']:
            for w in f['weather']:
                if datetime.datetime.fromtimestamp(f['dt']) > (datetime.datetime.now() + datetime.timedelta(days=days_to_forecast)):
                    break
                if len(changes) == 0 or changes[len(changes)-1]['forecast'] != w['description']:
                    changes.append({'forecast': w['description'],
                                    'start': datetime.datetime.fromtimestamp(f['dt']),
                                    'end': datetime.datetime.fromtimestamp(f['dt'])})
                elif changes[len(changes)-1]['forecast'] != w['description']:
                    changes[len(changes)-1]['end'] = datetime.datetime.fromtimestamp(f['dt'])

        change_str = []
        for change in changes:
            change_str.append(change['forecast'] + ' until ' + lib.dt.period_from_datetime(change['end']))

        return 'There will be ' + ' and then '.join((', '.join(change_str)).rsplit(', ', 1))
