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

def getStreamImage(isDay):
    # Capture an image stream to memory based on daymode
    with picamera.PiCamera() as camera:
        time.sleep(0.5)
        camera.resolution = (640, 480)
        with picamera.array.PiRGBArray(camera) as stream:
            if isDay:
                camera.exposure_mode = 'auto'
                camera.awb_mode = 'auto' 
            else:
                # Take Low Light image            
                # Set a framerate of 1/6fps, then set shutter
                # speed to 6s
                camera.framerate = Fraction(1, 6)
                camera.shutter_speed = 5
                camera.exposure_mode = 'off'
                camera.iso = 800
                # Give the camera a good long time to measure AWB
                # (you may wish to use fixed AWB instead)
                time.sleep( 10 )
            camera.capture(stream, format='rgb')
            return stream.array

def checkForMotion(data1, data2):
    sensitivity = self.config.get('Config', 'MotionSensitivity')
    # Find motion between two data streams based on sensitivity and threshold
    motionDetected = False
    pixChanges = 0;
    pixColor = 1 # red=0 green=1 blue=2
    for w in range(0, 640):
        for h in range(0, 480):
            # get the diff of the pixel. Conversion to int
            # is required to avoid unsigned short overflow.
            pixDiff = abs(int(data1[h][w][pixColor]) - int(data2[h][w][pixColor]))
            if  pixDiff > 10:
                pixChanges += 1
            if pixChanges > sensitivity:
                break; # break inner loop
        if pixChanges > sensitivity:
            break; #break outer loop.
    if pixChanges > sensitivity:
        motionDetected = True
    if motionDetected:
        dotCount = showDots(100 + 2)      # New Line        
        msgStr = "Found Motion - sensitivity=" + str(sensitivity) + " Exceeded ..."
        return True
    return False
