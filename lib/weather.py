#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
import decimal
import time
import pyowm

def weather_openweathermap(self, key):
	owm = pyowm.OWM(key)

	try:
		observation = owm.weather_at_id(2642182)
		w = observation.get_weather()
		l = observation.get_location()
		return ('Weather in ' + l.get_name() + ': ' + w.get_detailed_status() + '. ' + format(w.get_temperature('celsius')['temp'], '.1f')  + 'degrees')
	except Exception as e:
		return e
