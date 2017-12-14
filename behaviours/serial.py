from behaviours.behaviour import Behaviour

try:
    import serial
except ImportError as ex:
    pass


class Serial(Behaviour):

    routes = {
        '^.{1,3}$': 'serial_write'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)

    def serial_write(self):
        self.ser.write(str.encode(self.match.group().strip()))
        return 'Moving'
