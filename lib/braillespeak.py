#!/usr/bin/python
# -*- coding: latin-1 -*-
import serial
import time


def speak(self, message):
    if not self.config.get('Config', 'BraillespeakPort'):
        self.logging.info('Braillespeak disabled')
        return
    try:
        ser = serial.Serial(self.config.get('Config', 'BraillespeakPort'), 9600)
        time.sleep(5)  # @todo add process to thread to avoid delay
        ser.write(message)
        ser.close()
    except serial.serialutil.SerialException as e:
        self.logging.warning(str(e))
