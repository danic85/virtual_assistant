import nmap
from functools import partial

try:
    import RPi.GPIO as GPIO
except ImportError as e:
    pass
    # print str(e)

PIR_PIN = 4
PIR_LED_PIN = 17

SECURITY_OFF = 0
SECURITY_TEST = 1
SECURITY_ON = 2


def init(self):
    if hasattr(self, 'security') == False or self.security is None:
        self.security = SECURITY_OFF
    if hasattr(self, 'security_override') == False or self.security_override is None:
        self.security_override = False


def house_empty(self):
    if self.security_override:
        return ''

    if self.security == SECURITY_ON or self.security == SECURITY_OFF:
        empty = True
        macs_found = False

        # sudo nmap -sn 192.168.1.254/24 | egrep 'mac1|mac2'
        macs = self.config.get('Config', 'MacAddresses').split(',')
        nm = nmap.PortScanner()
        nm.scan(hosts=str(self.config.get('Config', 'RouterIP')) + '/24', arguments='-sP')
        for h in nm.all_hosts():
            if 'mac' in nm[h]['addresses']:
                macs_found = True
                if nm[h]['addresses']['mac'].lower() in macs:
                    empty = False

        if not macs_found:
            print ('Incorrect permissions. Do not assume empty')
            empty = False

        if empty:
            print 'House is empty'
            return on(self)
        else:
            print 'House is not empty'
            return off(self)

    return ''


def override(self):
    if not self.security_override:
        self.security_override = True
        return 'Security overridden'
    else:
        self.security_override = False
        return 'Security not overridden'


def test(self):
    response = on(self)
    if response is not None:
        self.security = SECURITY_TEST
    return response


def on(self):
    if self.security == SECURITY_OFF:
        self.logging.info('Starting PIR')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(PIR_LED_PIN, GPIO.OUT)
        GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=partial(motion_sensor, self), bouncetime=300)
        self.security = SECURITY_ON
        return 'Security Enabled'
    return None  # allow chatbot response


def off(self):
    if self.security != SECURITY_OFF:
        self.logging.info('Stopping PIR')
        GPIO.remove_event_detect(PIR_PIN)
        GPIO.cleanup()
        self.security = SECURITY_OFF
        return 'Security Disabled'
    return None  # allow chatbot response


# Callback function to run when motion detected
def motion_sensor(self, channel):
    GPIO.output(17, GPIO.LOW)
    if GPIO.input(4):     # True = Rising
        GPIO.output(17, GPIO.HIGH)
        if self.security == SECURITY_ON:
            self.logging.info('Taking Security Picture')
            self.do_command('camera')
