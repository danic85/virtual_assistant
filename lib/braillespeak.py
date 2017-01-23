#!/usr/bin/python
# -*- coding: latin-1 -*-
import serial

try:
  ser = serial.Serial('/dev/ttyUSB0', 9600)
except Exception e:
  print e.getMessage()

def speak(self):  
  ser.write(var)
#  ser.close()
