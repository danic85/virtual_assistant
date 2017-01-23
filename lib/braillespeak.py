#!/usr/bin/python
# -*- coding: latin-1 -*-
import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)

ser.write('hello\n')

c = input('enter a char: ')

ser.write(c.encode)

while 0:
    c = 'a' #input('Enter a char: ')
    if len(c) == 1:
        print c
        ser.write(c.encode())
#        print(ser.readline().decode().strip())
