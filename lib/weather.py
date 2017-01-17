#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyowm

def get(self):
    owm = pyowm.OWM(self.config.get('Config', 'OpenWeatherMapKey'))
    
    try:
        observation = owm.weather_at_id(2642182)
        w = observation.get_weather()
        l = observation.get_location()
        return ('Weather in ' + l.get_name() + ': ' + w.get_detailed_status() + '. ' + format(w.get_temperature('celsius')['temp'], '.1f')  + 'degrees')
    except Exception as e:
        self.logging.error(str(e))
        return "I can't check the weather at the moment"
