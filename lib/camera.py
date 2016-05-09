try:
    import picamera
except ImportError as e:
    print e

def snap():
    camera = picamera.PiCamera()
    try:
        camera.capture('image.jpg')
        pass
    finally:
        camera.close() 

def video():
    camera = picamera.PiCamera()
    try:
        camera.resolution = (640, 480)
        camera.start_recording('video.h264')
        camera.wait_recording(10)
        camera.stop_recording() 
    finally:
        camera.close()
