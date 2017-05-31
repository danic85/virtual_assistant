#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pyowm
import requests
from datetime import datetime
import calendar
from behaviours.behaviour import Behaviour


class Weather(Behaviour):

    routes = {
        'weather forecast': 'forecast',
        'weather$': 'get'
    }

    endpoints = {
        'forecast': 'http://api.openweathermap.org/data/2.5/forecast'
    }

    def get(self):
        owm = pyowm.OWM(self.config.get('Config', 'OpenWeatherMapKey'))

        try:
            observation = owm.weather_at_id(2642182)
            w = observation.get_weather()
            l = observation.get_location()
            return ('Weather in ' + l.get_name() + ': ' + w.get_detailed_status() + '. ' + format(
                w.get_temperature('celsius')['temp'], '.1f') + 'degrees')
        except Exception as e:
            self.logging.error(str(e))
            return "I can't check the weather at the moment"

    def forecast(self):
        args = [
            'appid=' + self.config.get('Config', 'OpenWeatherMapKey'),
            'id=2642182',
            'units=metric'
        ]
        forecast = requests.get(self.endpoints['forecast']+'?' + '&'.join(args)).json()

        occurrences = {'rain': set(), 'ice': set()}

        for f in forecast['list']:
            if f['main']['temp'] < 1:
                occurrences['ice'].add(f['dt'])

            for w in f['weather']:
                if 'Rain' in w['main']:
                    occurrences['rain'].add(datetime.fromtimestamp(f['dt']).weekday())

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
