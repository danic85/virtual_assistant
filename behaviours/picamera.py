#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
from behaviours.behaviour import Behaviour
from time import sleep
from fractions import Fraction

try:
    import picamera
except ImportError as ex:
    pass


class Picamera(Behaviour):

    routes = {
        '^camera$': 'take_photo',
        '^night vision$': 'take_night_photo',
        '^video$': 'take_video'
    }

    def take_photo(self):
        self.logging.info('Entering take_photo')
        self.logging.info('Load Camera')

        jpg = self.files + '/camera.jpg'

        try:
            camera = picamera.PiCamera(resolution=(1920, 1080))
            camera.hflip = True
            camera.vflip = True
            sleep(2)

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

