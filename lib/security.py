import time
try:
    import RPi.GPIO as GPIO
except ImportError as e:
    print str(e)

PIR_PIN = 7

SECURITY_OFF = 0
SECURITY_START = 1
SECURITY_ON = 2
SECURITY_STOP = 3
    
def house_empty(self):
    if (self.security == SECURITY_ON or self.security == SECURITY_OFF):
        empty = False
        
        # todo check who is home
        
        # Vendor list for MAC address
        # nm.scan('192.168.0.100/24', arguments='-O')
        # for h in nm.all_hosts():
        #     if 'mac' in nm[h]['addresses']:
        #         print(nm[h]['addresses'], nm[h]['vendor'])
        
        # if (empty):
        #     on()
        # else:
        #     off()
        
        
def on(self):
    self.security = SECURITY_START
    return 'Security Enabled'
    
def off(self):
    self.security = SECURITY_STOP
    return 'Security Disabled'
    
def sweep(self):
    # just exit if not running
    if (self.security == SECURITY_OFF):
        return
        
    try:
        # if security enabled
        if (self.security == SECURITY_ON):
            if GPIO.input(PIR_PIN):
                self.logging.info('Motion Detected!')
                self.doCommand('camera')
                
        # if initializing
        if (self.security == SECURITY_START):
            self.logging.info('Starting PIR')
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PIR_PIN, GPIO.IN)
            self.security = SECURITY_ON;
        
        # if shutting down
        if (self.security == SECURITY_STOP):
            self.logging.info('Stopping PIR')
            GPIO.cleanup()
            self.security = SECURITY_OFF
    except Exception as e:
        self.logging.error(str(e))
