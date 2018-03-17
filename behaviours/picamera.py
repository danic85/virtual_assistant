#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
from behaviours.behaviour import Behaviour
from time import sleep
from fractions import Fraction
import atexit

try:
    import RPi.GPIO as GPIO
except ImportError as e:
    pass

try:
    import picamera
    import wiringpi
except ImportError as ex:
    pass


class Picamera(Behaviour):

    CAMERA_MOVEABLE = False  # Set to True if camera is mounted to servo to hide when not in use
    CAMERA_OPEN_POS = 200
    CAMERA_CLOSE_POS = 50
    CAMERA_DEFAULT_POS = CAMERA_CLOSE_POS  # Determines if camera is open or closed by default

    routes = {
        '^photo': 'take_photo',
        '^camera$': 'open_and_take_photo',
        '^night vision$': 'take_night_photo',
        '^open camera$': 'open_camera',
        '^close camera$': 'close_camera',
        '^video$': 'open_and_take_video',
        '^timelapse': 'timelapse',
        '^stop timelapse$': 'stop_timelapse'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.security_override = False

        if self.CAMERA_MOVEABLE:
            try:
                # use 'GPIO naming'
                wiringpi.wiringPiSetupGpio()

                # set #18 to be a PWM output
                wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

                # set the PWM mode to milliseconds stype
                wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

                # divide down clock
                wiringpi.pwmSetClock(192)
                wiringpi.pwmSetRange(2000)

                # set servo to default position to start
                self.move_camera(self.CAMERA_DEFAULT_POS)

                atexit.register(self.close_camera())  # exit handler, close camera on exiting application
            except Exception as ex:
                pass

    def move_camera(self, position):
        if self.CAMERA_MOVEABLE:
            try:
                wiringpi.pwmWrite(18, position)
            except Exception as ex:
                pass
        return None

    def open_camera(self):

        GPIO.output(self.LED_IR, GPIO.HIGH)
        return self.move_camera(self.CAMERA_OPEN_POS)

    def close_camera(self):
        GPIO.output(self.LED_IR, GPIO.LOW)
        return self.move_camera(self.CAMERA_DEFAULT_POS)

    def timelapse(self):
        self.define_idle(self.open_and_take_photo, 0)  # take a photo every 5 minutes
        return 'Timelapse started'

    def stop_timelapse(self):
        if self.remove_idle(self.open_and_take_photo):
            return 'Timelapse stopped'
        return 'No timelapse to stop'

    def open_and_take_photo(self):
        """ Open camera if mounted to servo and take photo, then return to default position """
        self.open_camera()
        sleep(3)
        response = self.take_photo()
        self.close_camera()
        return response

    def take_photo(self):
        """ Take photo using PI camera. Works with night vision camera in all light levels."""
        self.logging.info('Entering take_photo')
        self.logging.info('Load Camera')

        jpg = self.files + '/camera.jpg'

        try:
            # camera = picamera.PiCamera(resolution=(1920, 1080))
            camera = picamera.PiCamera(resolution=(800, 600))
            # camera.hflip = True
            # camera.vflip = True
            # sleep(2)

        except Exception as e:
            self.logging.error(str(e))
            return 'Could not load camera'

        self.logging.info('Taking Photo...')

        try:
            response = camera.capture(jpg)
            pass
        except Exception as e:
            self.logging.error(str(e))
            return 'Could not take picture'
        finally:
            self.logging.info('Closing Camera...')
            camera.close()
            self.logging.info('Closed.')

        if response:
            self.logging.info('Returning response.')
            return response
        self.act.respond_photo(jpg)

        self.logging.info('Exiting take_photo')
        return None

    def take_night_photo(self):
        """ Standard PI camera can take night vision shots with this. Very slow. """
        self.logging.info('Entering take_night_photo')
        jpg = self.files + '/camera.jpg'

        try:
            camera = picamera.PiCamera(
                resolution=(1280, 720),
                framerate=Fraction(1, 6),
                sensor_mode=3)
            camera.hflip = True
            camera.vflip = True
            camera.shutter_speed = 6000000
            camera.iso = 800
            # Turn the camera's LED off
            camera.led = False
            # Give the camera a good long time to set gains and
            # measure AWB (you may wish to use fixed AWB instead)
            sleep(30)
            camera.exposure_mode = 'off'
            # Finally, capture an image with a 6s exposure. Due
            # to mode switching on the still port, this will take
            # longer than 6 seconds
            camera.capture(jpg)
            camera.close()

        except Exception as e:
            self.logging.error(str(e))
            return 'Could not load camera'

        self.act.respond_photo(jpg)
        self.logging.info('Exiting take_night_photo')
        return None

    def open_and_take_video(self):
        self.open_camera()
        sleep(3)
        response = self.take_video()
        self.move_camera(self.CAMERA_DEFAULT_POS)
        return response

    def take_video(self):
        h264 = self.files + '/video.h264'
        mp4 = self.files + '/video.mp4'

        try:
            camera = picamera.PiCamera()
            camera.hflip = True
            camera.vflip = True
        except Exception as e:
            self.logging.error(str(e))
            return 'Could not load camera'

        try:
            camera.resolution = (640, 480)
            camera.start_recording(h264)
            camera.wait_recording(10)
            camera.stop_recording()
        except Exception as e:
            self.logging.error(str(e))
            return 'Could not record video'
        finally:
            camera.close()

        p = subprocess.Popen('MP4Box -add ' + h264 + ' ' + mp4, stdout=subprocess.PIPE, shell=True)
        for line in p.communicate():
            print(line)
        p.wait()
        print(p.returncode)

        os.remove(h264)
        self.act.respond_video(mp4)
        return None

