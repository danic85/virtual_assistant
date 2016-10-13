import subprocess
import os
# import logging

try:
    import picamera
except ImportError as e:
    print e
    # logging.info(e)
    

def take_photo(self, bot, logging):
    logging.info('Entering take_photo')
    logging.info('Load Camera')
    camera = picamera.PiCamera()
    logging.info('Taking Photo...')
    try:
        response = camera.capture('image.jpg')
        logging.info('Response: ' + response)
        pass
    finally:
        logging.info('Closing Camera...')
        camera.close()
        logging.info('Closed.')
    
    if response:
        logging.info('Returning response.')
        return response
    logging.info('Opening file')
    f = open('image.jpg', 'rb')  # file on local disk
    logging.info('Sending photo')
    response = bot.sendPhoto(self.user, f)
    logging.info('Removing photo')
    os.remove('image.jpg') # don't save it!
    logging.info('Exiting take_photo')
    return ''

def take_video(self, bot):
    camera = picamera.PiCamera()
    try:
        camera.resolution = (640, 480)
        camera.start_recording('video.h264')
        camera.wait_recording(10)
        camera.stop_recording() 
    finally:
        camera.close()
    
    p = subprocess.Popen('MP4Box -add video.h264 video.mp4', stdout=subprocess.PIPE, shell=True)
    for line in p.communicate():
         print line
    p.wait()
    print p.returncode
    
    f = open('video.mp4', 'rb')
    response = bot.sendVideo(self.user, f)
    os.remove('video.mp4')
    os.remove('video.h264')

    return ''
