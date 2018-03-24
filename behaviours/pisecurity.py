#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nmap
from functools import partial
from time import sleep
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

    PIR_PIN = 18
    PIR_LED_PIN = 17

    SECURITY_OFF = 0
    SECURITY_TEST = 1
    SECURITY_ON = 2

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.assistant = kwargs.get('assistant', None)
        self.security = self.SECURITY_OFF
        self.security_override = False

    def test(self):
        response = self.on()
        if response is not None:
            self.security = self.SECURITY_TEST
            # test LED output
            GPIO.output(self.PIR_LED_PIN, GPIO.HIGH)
            sleep(2)
            GPIO.output(self.PIR_LED_PIN, GPIO.LOW)

        return response + ' (Test)'

    def on(self):
        if self.security == self.SECURITY_OFF:
            try:
                self.logging.info('Starting PIR')
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(self.PIR_LED_PIN, GPIO.OUT)
                GPIO.add_event_detect(self.PIR_PIN, GPIO.BOTH, self.__motion_sensor, bouncetime=300)
                self.security = self.SECURITY_ON
                self.act.chain_command('open camera')
                return 'Security Enabled'
            except NameError as e:
                return 'Could not start security: ' + str(e)
        return None

    def off(self):
        if self.security != self.SECURITY_OFF:
            try:
                self.logging.info('Stopping PIR')
                GPIO.remove_event_detect(self.PIR_PIN)
                self.security = self.SECURITY_OFF
                self.act.chain_command('close camera')
                return 'Security Disabled'
            except NameError as e:
                return 'Could not stop security: ' + str(e)
        return None

    # Callback function to run when motion detected
    def __motion_sensor(self, PIR_PIN):
        GPIO.output(self.PIR_LED_PIN, GPIO.LOW)
        if GPIO.input(self.PIR_PIN):  # True = Rising
            GPIO.output(self.PIR_LED_PIN, GPIO.HIGH)
            if self.security == self.SECURITY_ON:
                self.logging.info('Taking Security Picture')
                if self.assistant is not None:
                    msg = {"chat": {"id": self.assistant.config.get_or_request('Admin')}, "text": 'photo'}
                    self.assistant.handle(msg)  # chain command doesn't work inside a callback
                else:
                    self.logging.error('Assistant not set')
