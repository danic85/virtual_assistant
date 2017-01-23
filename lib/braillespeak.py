#!/usr/bin/python
# -*- coding: latin-1 -*-
import serial

def speak(self):
  ser = serial.Serial('/dev/ttyUSB0', 9600)
  ser.write(var)
  ser.close()
