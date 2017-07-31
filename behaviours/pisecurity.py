#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nmap
from functools import partial
from behaviours.behaviour import Behaviour

try:
    import RPi.GPIO as GPIO
except ImportError as e:
    pass


class Pisecurity(Behaviour):

    routes = {
        '^security on$': 'on',
        '^security off$': 'off',
        '^test security$': 'test'
    }

    PIR_PIN = 4
    PIR_LED_PIN = 17

    SECURITY_OFF = 0
    SECURITY_TEST = 1
    SECURITY_ON = 2

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.security = self.SECURITY_OFF
        self.security_override = False

    def test(self):
        response = self.on()
        if response is not None:
            self.security = self.SECURITY_TEST
        return response

    def on(self):
        if self.security == self.SECURITY_OFF:
            try:
                self.logging.info('Starting PIR')
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(self.PIR_LED_PIN, GPIO.OUT)
                GPIO.add_event_detect(self.PIR_PIN, GPIO.BOTH, callback=partial(self.__motion_sensor, self), bouncetime=300)
                self.security = self.SECURITY_ON
                return 'Security Enabled'
            except NameError as e:
                return 'Could not start security: ' + str(e)
        return None

    def off(self):
        if self.security != self.SECURITY_OFF:
            try:
                self.logging.info('Stopping PIR')
                GPIO.remove_event_detect(self.PIR_PIN)
                GPIO.cleanup()
                self.security = self.SECURITY_OFF
                return 'Security Disabled'
            except NameError as e:
                return 'Could not stop security: ' + str(e)
        return None

    # Callback function to run when motion detected
    def __motion_sensor(self):
        GPIO.output(17, GPIO.LOW)
        if GPIO.input(4):  # True = Rising
            GPIO.output(17, GPIO.HIGH)
            if self.security == self.SECURITY_ON:
                self.logging.info('Taking Security Picture')
                self.act.chain_command('camera')
