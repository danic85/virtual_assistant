import picamera

def snap():
  camera = picamera.PiCamera()
  camera.capture('image.jpg')
