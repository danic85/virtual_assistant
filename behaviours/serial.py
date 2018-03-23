from behaviours.behaviour import Behaviour

try:
    import serial
except ImportError as ex:
    pass


class Serial(Behaviour):
    """ A test class for serial communication with Arduino. For more code see the 'arduino' branch.
    """
    routes = {
        '^.{1,3}$': 'serial_write',
        '^speak .+': 'serial_speak'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        except serial.serialutil.SerialException as ex:
            pass

    def serial_write(self):
        if self.match.group().strip().lower() != 'ms':
            self.act.respond_keyboard(['mf', 'mb', 'ml', 'mr', 'ms']) #  display keyboard buttons for easy movement
        else:
            self.act.respond_keyboard([])
            self.act.respond('Stopping')
            return

        try:
            self.ser.write(str.encode(self.match.group().strip().lower()))
        except AttributeError as ex:
            pass
        return 'Moving'

    def serial_speak(self):
        try:
            self.ser.write(str.encode(self.match.group().strip().lower()))
        except AttributeError as ex:
            pass
        return 'Speaking'