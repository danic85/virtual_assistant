

import datetime, unittest
import os, sys
from mock import Mock, call, patch

# sys.path.append(os.path.abspath('..'))
# import behaviours
from behaviours import general
from lib.interaction import Interaction
from lib.config import Config
import re

class TestGeneralMethods(unittest.TestCase):
    def test_routes(self):
        b = general.General(db=None, config={}, dir='')
        act = Interaction()
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        b.log_expense = Mock()
        b.config_set = Mock()
        b.time = Mock()
        b.datetime = Mock()

        response = b.handle(act)
        self.assertEqual(response, None)

        act.command = {'text': 'time'}
        b.handle(act)
        b.time.assert_called_once()

        act.command = {'text': 'set config something=avalue'}
        b.handle(act)
        b.config_set.assert_called_once()
        self.assertEqual(b.match.group(1), 'something')
        self.assertEqual(b.match.group(2), 'avalue')

        b.config_set = Mock()
        act.command = {'text': 'config something=anothervalue'}
        b.handle(act)
        b.config_set.assert_called_once()
        self.assertEqual(b.match.group(1), 'something')
        self.assertEqual(b.match.group(2), 'anothervalue')

        b.config_set = Mock()
        act.command = {'text': 'config something:avalue'}
        b.handle(act)
        b.config_set.assert_called_once()
        self.assertEqual(b.match.group(1), 'something')
        self.assertEqual(b.match.group(2), 'avalue')

    def test_set_config(self):
        b = general.General(db=None, config=Config(), dir='')
        act = Interaction()
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)
        b.config.db = Mock()
        b.config.db.insert = Mock(return_value=1234)

        b.match = re.search('^(?:set )?config (.*)(?:=|\:)(.*)$', 'set config configItem=value',
                            re.IGNORECASE)

        self.assertEquals(b.config_set(), 'Config set')
        b.config.db.insert.assert_called_with('config', {'key': 'configItem', 'value': 'value'})

    def test_get_config(self):
        b = general.General(db=None, config=Config(), dir='')
        act = Interaction()
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)
        b.config.db = Mock()
        b.config.db.find_one = Mock(return_value=None)
        try:
            self.assertEquals(b.config_get('something'), None)
        except ValueError as e:
            self.assertEqual(str(e), 'something is not set in config')

        b.config.db.find_one = Mock(return_value={'key': 'configItem', 'value': '1234'})
        self.assertEquals(b.config_get('something'), '1234')




    #     def test_morning(self):
#         bot = self.build_bot()
#         # countdown = Mock(return_value = 'countdown response')
#         response = morning(bot)
#         bot.chat.respond.assert_called_with('good morning', 1)
#         calls = [call('get closest countdowns'), call('weather forecast'), call('budget'), call('thought of the day'), call('did you know')]
#         bot.do_command.assert_has_calls(calls)
#         self.assertNotEqual(response, '')
#         self.assertNotEqual(response, None)
#
#     def test_morning_others(self):
#         bot = self.build_bot()
#         response = morning_others(bot)
#         bot.chat.respond.assert_called_with('good morning', 1)
#         calls = [call('get closest countdowns'), call('budget'), call('weather forecast'), call('thought of the day'), call('did you know')]
#         bot.do_command.assert_has_calls(calls)
#         self.assertNotEqual(response, '')
#         self.assertNotEqual(response, None)
#
#     def test_broadcast(self):
#         bot = self.build_bot()
#         response = broadcast(bot)
#         self.assertEqual(response, bot.command.replace('broadcast ', '', 1))
#         bot.config.get.assert_called_with('Config','Users')
#         self.assertEqual(bot.user, bot.config.get('Config','Users').split(','))
#
    def test_time(self):
        g = general.General(db=None, config={}, dir='')
        self.assertEqual(g.time(), datetime.datetime.now().strftime('%I:%M %p'))

    def test_datetime(self):
        g = general.General(db=None, config={}, dir='')
        self.assertEqual(g.date_time(), datetime.datetime.now().strftime('%d-%m-%y %I:%M %p'))
#
#     # @patch('__builtin__.open')
#     # def test_set_countdown(self, open_mock):
#     #     bot = self.build_bot()
#     #     bot.files = 'dir'
#     #     bot.command = Mock(return_value='command 01-01-2017 test event')
#     #     open_mock.return_value = 'file'
#     #     response = set_countdown(bot)
#     #     open_mock.assert_called_with('dir/mojo_debug.log', 'r')
#
#     def test_command_list(self):
#         bot = self.build_bot()
#         bot.commandList = [{'1','test'},{'2','test'}]
#         response = "Available commands:\n"
#         for key, val in bot.commandList:
#             response += key + "\n"
#         self.assertEqual(command_list(bot), response)
#
#     @patch('__builtin__.open')
#     def test_get_log(self, open_mock):
#         bot = self.build_bot()
#         bot.sendDocument = Mock()
#         bot.dir = 'dir'
#         bot.files = 'dir/files'
#         open_mock.return_value = 'file'
#         response = get_log(bot)
#         open_mock.assert_called_with('dir/files/mojo_debug.log', 'r')
#         bot.sendDocument.assert_called_with(bot.user, 'file')
#         self.assertEqual(response, '')
#
#     def build_bot(self):
#         bot = Mock(return_value = 456)
#         bot.chat = Mock()
#         bot.admin = 1
#         bot.chat.respond = Mock(return_value = 'chat response')
#         bot.do_command = Mock(return_value = 'command response')
#         bot.config = Mock()
#         bot.config.get = Mock(return_value = '1,2')
#         return bot
#
if __name__ == '__main__':
    unittest.main()