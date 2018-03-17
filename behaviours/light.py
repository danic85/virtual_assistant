#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behaviours.behaviour import Behaviour

try:
    import RPi.GPIO as GPIO
except ImportError as e:
    pass

class Light(Behaviour):

    routes = {
        '^(light on|light|lumos)$': 'all',
        '^(light off|nox)$': 'off',
        '^red light$': 'red',
        '^green light$': 'green',
        '^blue light$': 'blue',
        '^purple light$': 'purple',
        '^cyan light$': 'cyan',
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def on(self, r, g, b):
        try:
            self.off()
            if r:
                GPIO.output(self.LED_RED, GPIO.HIGH)
            if g:
                GPIO.output(self.LED_GREEN, GPIO.HIGH)
            if b:
                GPIO.output(self.LED_BLUE, GPIO.HIGH)
            return 'Light on'
        except NameError as e:
            return 'Could not turn light on: ' + str(e)

    def off(self):
        try:
            GPIO.output(self.LED_RED, GPIO.LOW)
            GPIO.output(self.LED_GREEN, GPIO.LOW)
            GPIO.output(self.LED_BLUE, GPIO.LOW)
            return 'Light off'
        except NameError as e:
            return 'Could not turn light off: ' + str(e)

    def all(self):
        return self.on(True, True, True)

    def red(self):
        return self.on(True, False, False)

    def green(self):
        return self.on(False, True, False)

    def blue(self):
        return self.on(False, False, True)

    def purple(self):
        return self.on(True, False, True)

    def yellow(self):
        return self.on(True, True, False)

    def cyan(self):
        return self.on(False, True, True)
