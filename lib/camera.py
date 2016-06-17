try:
    import picamera
except ImportError as e:
    print e
    

def take_photo(self):
    camera = picamera.PiCamera()
    try:
        response = camera.capture('image.jpg')
        pass
    finally:
        camera.close() 
    
    if response:
        return response
    f = open('image.jpg', 'rb')  # file on local disk
    response = bot.sendPhoto(self.user, f)
    os.remove('image.jpg') # don't save it!
    return ''

def take_video(self):
    camera = picamera.PiCamera()
    try:
        camera.resolution = (640, 480)
        camera.start_recording('video.h264')
        camera.wait_recording(10)
        camera.stop_recording() 
    finally:
        camera.close()
    
    if response:
       return response
    
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
