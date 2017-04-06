import subprocess
import os

try:
    import picamera
except ImportError as ex:
    pass
    # print str(ex)


def take_photo(self):
    self.logging.info('Entering take_photo')
    self.logging.info('Load Camera')

    jpg = self.files + '/camera.jpg'

    try:
        camera = picamera.PiCamera()
        camera.hflip = True
        camera.vflip = True

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
    self.logging.info('Opening file')
    f = open(jpg, 'rb')  # file on local disk
    self.logging.info('Sending photo')
    if self.user:
        self.sendPhoto(self.user, f)
    else:
        self.sendPhoto(self.admin, f)
    self.logging.info('Removing photo')
    os.remove(jpg)  # don't save it!
    self.logging.info('Exiting take_photo')
    return ''


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
        return 'Could not take picture'
    finally:
        camera.close()

    p = subprocess.Popen('MP4Box -add ' + h264 + ' ' + mp4, stdout=subprocess.PIPE, shell=True)
    for line in p.communicate():
        print line
    p.wait()
    print p.returncode

    f = open(mp4, 'rb')
    self.sendVideo(self.user, f)
    os.remove(mp4)
    os.remove(h264)

    return ''
