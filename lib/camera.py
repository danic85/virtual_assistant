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
