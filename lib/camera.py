import subprocess
import os

try:
    import picamera
except ImportError as e:
    print str(e)

def take_photo(self):
    self.logging.info('Entering take_photo')
    self.logging.info('Load Camera')
    try:
        camera = picamera.PiCamera()
    except Exception as e:
        self.logging.error(str(e))
        return 'Could not load camera'
        
    self.logging.info('Taking Photo...')
    
    try:
        response = camera.capture('image.jpg')
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
    f = open('image.jpg', 'rb')  # file on local disk
    self.logging.info('Sending photo')
    response = self.sendPhoto(self.user, f)
    self.logging.info('Removing photo')
    os.remove('image.jpg') # don't save it!
    self.logging.info('Exiting take_photo')
    return ''

def take_video(self):
    try:
        camera = picamera.PiCamera()
    except Exception as e:
        self.logging.error(str(e))
        return 'Could not load camera'
    
    try:
        camera.resolution = (640, 480)
        camera.start_recording('video.h264')
        camera.wait_recording(10)
        camera.stop_recording() 
    except Exception as e:
        self.logging.error(str(e))
        return 'Could not take picture'
    finally:
        camera.close()
    
    p = subprocess.Popen('MP4Box -add video.h264 video.mp4', stdout=subprocess.PIPE, shell=True)
    for line in p.communicate():
         print line
    p.wait()
    print p.returncode
    
    f = open('video.mp4', 'rb')
    response = self.sendVideo(self.user, f)
    os.remove('video.mp4')
    os.remove('video.h264')

    return ''
