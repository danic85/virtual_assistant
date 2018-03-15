#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behaviours.behaviour import Behaviour

try:
    import RPi.GPIO as GPIO
except ImportError as e:
    pass


class Light(Behaviour):

    routes = {
        '^light on$': 'on',
        '^light off$': 'off'
    }

    LED_PIN_RED = 17

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def on(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.LED_PIN_RED, GPIO.OUT)
            GPIO.output(self.LED_PIN_RED, GPIO.HIGH)
            return 'Light on'
        except NameError as e:
            return 'Could not turn light on: ' + str(e)

    def off(self):
        try:
            GPIO.output(self.LED_PIN_RED, GPIO.LOW)
            GPIO.cleanup()
            return 'Light off'
        except NameError as e:
            return 'Could not turn light off: ' + str(e)
