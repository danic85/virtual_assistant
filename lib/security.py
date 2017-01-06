import time
import nmap
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
    if (hasattr(self, 'security_override') == True and self.security_override == True):
        return ''
        
    if (hasattr(self, 'security') == False):
        self.security = SECURITY_OFF
        
    if (self.security == SECURITY_ON or self.security == SECURITY_OFF):
        empty = True
        
        import nmap

        #sudo nmap -sn 192.168.1.254/24 | egrep 'mac1|mac2'
        macs = self.config.get('Config', 'MacAddresses').split(',')
        nm = nmap.PortScanner()
        nm.scan(hosts=str(self.config.get('Config', 'RouterIP'))+'/24', arguments='-sP')
        for h in nm.all_hosts():
            if 'mac' in nm[h]['addresses']:
                if nm[h]['addresses']['mac'] in macs:
                        empty = False
            else:
                # Incorrect permissions. Do not assume empty
                empty = False;

        if (empty):
            print 'House is empty'
            return on()
        else:
            print 'House is not empty'
            return off()
        
    return ''
    
def override(self):
    if (hasattr(self, 'security_override') == False or self.security_override == False):
        self.security_override = True
        return 'Security overridden'
    else:
        self.security_override = False
        return 'Security not overridden'

def on(self):
    if (self.security != SECURITY_ON):
        self.security = SECURITY_START
        return 'Security Enabled'
    return ''
    
def off(self):
    if (self.security != SECURITY_OFF):
        self.security = SECURITY_STOP
        return 'Security Disabled'
    return ''
    
def sweep(self):
    # just exit if not running
    try:
        if (hasattr(self, 'security') == False or self.security == SECURITY_OFF or self.security is None):
            return str(SECURITY_OFF)
            
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
        self.logging.info(str(self.security))
        return str(self.security)
    except Exception as e:
        self.logging.error(str(e))