#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
from behaviours.behaviour import Behaviour
from time import sleep
from fractions import Fraction
import atexit
from lib import pydrive
import datetime

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

    LED_IR = 10
    camera = None
    jpg = None
    h264 = None
    mp4 = None

    routes = {
        '^camera$': 'open_and_take_photo_small',
        "what's going on": 'open_and_take_photo_small',
        '^big photo': 'open_and_take_photo',
        '^night vision$': 'take_night_photo',
        '^open camera$': 'open_camera',
        '^close camera$': 'close_camera',
        '^video$': 'open_and_take_video',
        '^timelapse to drive': 'timelapse_to_drive',
        '^timelapse$': 'timelapse',
        '^stop timelapse$': 'stop_timelapse',
        'pydrive': 'take_photo_pydrive'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.jpg = self.files + '/camera.jpg'
        self.h264 = self.files + '/video.h264'
        self.mp4 = self.files + '/video.mp4'

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.LED_IR, GPIO.OUT)
            GPIO.output(self.LED_IR, GPIO.LOW)  # turn IR off (in case they were switched on and then a crash occurred)
        except Exception as ex:
            pass

    def open_camera(self, width, height):
        try:
            GPIO.output(self.LED_IR, GPIO.HIGH)
            sleep(1)
            self.camera = picamera.PiCamera(resolution=(width, height))
            sleep(1)
            # camera.hflip = True
            # camera.vflip = True
        except Exception as e:
            self.logging.error(str(e))
            return 'Could not open camera'

        return None

    def close_camera(self):
        try:
            GPIO.output(self.LED_IR, GPIO.LOW)
            self.logging.info('Closing Camera...')
            self.camera.close()
            self.logging.info('Closed.')
        except Exception as e:
            self.logging.error(str(e))
            return 'Could not close camera'
        return None

    def timelapse(self):
        """ Take photo and send to admin every 5 minutes. """
        self.define_idle(self.open_and_take_photo, 0)  # take a photo every 5 minutes
        return 'Timelapse started'

    def timelapse_to_drive(self):
        """ Take photo and send to google drive every 5 minutes. """
        self.define_idle(self.take_photo_pydrive, 0)  # take a photo every 5 minutes
        return 'Timelapse to drive started'

    def stop_timelapse(self):
        if self.remove_idle(self.open_and_take_photo) or self.remove_idle(self.take_photo_pydrive):
            return 'Timelapse stopped'
        return 'No timelapse to stop'

    def take_photo_pydrive(self):
        self.open_camera(1920, 1080)
        response = self.take_photo()
        self.close_camera()

        try:
            drive = pydrive.authenticate()

            pi_files_dir = pydrive.getFolderId(drive, 'root', 'Pi Files')
            if pi_files_dir is None:
                pi_files_dir = pydrive.createFolder(drive, 'root', 'Pi Files')

            photos_dir = pydrive.getFolderId(drive, pi_files_dir, 'Photos')
            if photos_dir is None:
                photos_dir = pydrive.createFolder(drive, pi_files_dir, 'Photos')

            today = datetime.datetime.now().strftime('%Y-%m-%d')
            today_dir = pydrive.getFolderId(drive, photos_dir, today)
            if today_dir is None:
                today_dir = pydrive.createFolder(drive, photos_dir, today)

            if today_dir:
                file1 = drive.CreateFile(
                    {"parents": [{"kind": "drive#fileLink", "id": today_dir}],
                     'title': datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
                     })
                file1.SetContentFile(self.jpg)
                file1.Upload()
        except Exception as e:
            return e

        return response

    def open_and_take_photo(self):
        """ Open camera if mounted to servo and take photo, then return to default position """
        self.open_camera(1920, 1080)
        response = self.take_photo()
        if response is None:
            self.act.respond_photo(self.jpg)
        self.close_camera()
        return response

    def open_and_take_photo_small(self):
        """ Open camera if mounted to servo and take photo, then return to default position """
        self.open_camera(640, 480)
        response = self.take_photo()
        if response is None:
            self.act.respond_photo(self.jpg)
        self.close_camera()
        return response

    def take_photo(self):
        """ Take photo using PI camera. Works with night vision camera in all light levels."""
        self.logging.info('Taking Photo...')
        try:
            response = self.camera.capture(self.jpg)
            # sleep(2)
            pass
        except Exception as e:
            self.logging.error(str(e))
            return 'Could not take picture'

        if response:
            self.logging.info('Returning response.')
            return response

        self.logging.info('Exiting take_photo')
        return None

    def take_night_photo(self):
        """ Standard PI camera can take night vision shots with this. Very slow. """
        self.logging.info('Entering take_night_photo')
        self.open_camera(1280, 720)

        try:
            self.camera.framerate = Fraction(1, 6)
            self.camera.sensor_mode = 3
            self.camera.hflip = True
            self.camera.vflip = True
            self.camera.shutter_speed = 6000000
            self.camera.iso = 800
            # Turn the camera's LED off
            self.camera.led = False
            # Give the camera a good long time to set gains and
            # measure AWB (you may wish to use fixed AWB instead)
            sleep(30)
            self.camera.exposure_mode = 'off'
            # Finally, capture an image with a 6s exposure. Due
            # to mode switching on the still port, this will take
            # longer than 6 seconds
            self.camera.capture(self.jpg)
            self.close_camera()

        except Exception as e:
            self.logging.error(str(e))
            return 'Could not load camera'

        self.act.respond_photo(self.jpg)
        self.logging.info('Exiting take_night_photo')
        return None

    def open_and_take_video(self):
        self.open_camera(640, 480)
        response = self.take_video()
        return response

    def take_video(self):
        try:
            self.logging.info('Recording video...')
            self.camera.start_recording(self.h264)
            self.camera.wait_recording(10)
            self.logging.info('Stopping...')
            self.camera.stop_recording()
            self.logging.info('Stopped')
        except Exception as e:
            self.logging.error(str(e))
            return 'Could not record video'
        finally:
            self.close_camera()

        self.logging.info('Processing Video...')
        p = subprocess.Popen('MP4Box -add ' + self.h264 + ' ' + self.mp4, stdout=subprocess.PIPE, shell=True)
        for line in p.communicate():
            print(line)
        p.wait()
        print(p.returncode)
        self.logging.info('Done.')

        os.remove(self.h264)
        self.act.respond_video(self.mp4)
        return None
