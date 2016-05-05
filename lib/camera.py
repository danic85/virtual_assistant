try:
    import picamera
except ImportError as e:
    print e

def snap():
  camera = picamera.PiCamera()
  camera.capture('image.jpg')
