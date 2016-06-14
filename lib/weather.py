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

	# Search for current weather in London (UK)
	observation = owm.weather_around_coords(-1.69, 55.17)
	w = observation.get_weather()
	return (w.get_status() + '. ' + format(w.get_temperature('celsius')['temp'], '.1f')  + 'degrees')
