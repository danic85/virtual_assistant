try:
    import picamera
except ImportError as e:
    print "Import picamera error: {0}".format(str(e))

def snap():
  try:
    camera = picamera.PiCamera()
    camera.capture('image.jpg')
  except Exception as e:
    return 'could not take picture error: {0}'.format(str(e))
