from braillespeak import speak
import datetime, unittest, serial
from mock import Mock, call, patch


class TestBraillespeakMethods(unittest.TestCase):
    @patch('serial.Serial')
    def test_speak(self, mock_serial):
        bot = Mock()
        bot.logging = Mock()
        speak(bot, 'test')
        bot.logging.warning.assert_not_called()

    @patch('serial.Serial')
    def test_speak_error(self, mock_serial):
        mock_serial.side_effect = serial.serialutil.SerialException()
        bot = Mock()
        bot.logging = Mock()
        speak(bot, 'test')
        bot.logging.warning.assert_called()

if __name__ == '__main__':
    unittest.main()