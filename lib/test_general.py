from general import time, morning, morning_others, broadcast, date_time, command_list, update_self, get_log
import datetime, unittest
from mock import Mock, call, patch


class TestGeneralMethods(unittest.TestCase):

    def test_morning(self):
        bot = self.build_bot()
        countdown = Mock(return_value = 'countdown response')
        response = morning(bot)
        bot.chat.respond.assert_called_with('good morning', 1)
        calls = [call('weather'), call('budget'), call('thought of the day'), call('did you know')]
        bot.do_command.assert_has_calls(calls)
        self.assertNotEqual(response, '')
        self.assertNotEqual(response, None)
        
    def test_morning_others(self):
        bot = self.build_bot()
        response = morning_others(bot)
        bot.chat.respond.assert_called_with('good morning', 1)
        calls = [call('budget'), call('weather'), call('thought of the day'), call('did you know')]
        bot.do_command.assert_has_calls(calls)
        self.assertNotEqual(response, '')
        self.assertNotEqual(response, None)
        
    def test_broadcast(self):
        bot = self.build_bot()
        response = broadcast(bot)
        self.assertEqual(response, bot.command.replace('broadcast ', '', 1))
        bot.config.get.assert_called_with('Config','Users')
        self.assertEqual(bot.user, bot.config.get('Config','Users').split(','))
        
    def test_time(self):
        self.assertEqual(time(self), datetime.datetime.now().strftime('%I:%M %p'))
        
    def test_datetime(self):
        self.assertEqual(date_time(self), datetime.datetime.now().strftime('%d-%m-%y %I:%M %p'))
        
    # @patch('__builtin__.open')
    # def test_set_countdown(self, open_mock):
    #     bot = self.build_bot()
    #     bot.files = 'dir'
    #     bot.command = Mock(return_value='command 01-01-2017 test event')
    #     open_mock.return_value = 'file'
    #     response = set_countdown(bot)
    #     open_mock.assert_called_with('dir/mojo_debug.log', 'r')
    
    def test_command_list(self):
        bot = self.build_bot()
        bot.commandList = [{'1','test'},{'2','test'}]
        response = "Available commands:\n"
        for key, val in bot.commandList:
            response += key + "\n"
        self.assertEqual(command_list(bot), response)
        
    @patch('__builtin__.open')
    def test_get_log(self, open_mock):
        bot = self.build_bot()
        bot.sendDocument = Mock()
        bot.dir = 'dir'
        open_mock.return_value = 'file'
        response = get_log(bot)
        open_mock.assert_called_with('dir/mojo_debug.log', 'r')
        bot.sendDocument.assert_called_with(bot.user, 'file')
        self.assertEqual(response, '')
        
    def build_bot(self):
        bot = Mock(return_value = 456)
        bot.chat = Mock()
        bot.admin = 1
        bot.chat.respond = Mock(return_value = 'chat response')
        bot.do_command = Mock(return_value = 'command response')
        bot.config = Mock()
        bot.config.get = Mock(return_value = '1,2')
        return bot

if __name__ == '__main__':
    unittest.main()