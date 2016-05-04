try:
    import picamera
except ImportError:
    print 'no picamera'

def snap():
  try:
    camera = picamera.PiCamera()
    camera.capture('image.jpg')
  except Exception:
    print 'could not take picture'
