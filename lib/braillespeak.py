#!/usr/bin/python
# -*- coding: latin-1 -*-
import serial, time


def speak(self, message):
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        # time.sleep(3) # this is necessary when using @todo add process to thread
        ser.write(message)
        ser.close()
    except serial.serialutil.SerialException as e:
        self.logging.warning(str(e))
