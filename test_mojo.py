#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime, os, unittest
import mojo, aiml, ConfigParser
from mock import Mock, call, patch
from freezegun import freeze_time


class TestMojoMethods(unittest.TestCase):
    def test_mojo(self):
        ConfigParser.ConfigParser = Mock()
        bot = mojo.Mojo()
        self.assertEqual(bot.dir, os.path.dirname(os.path.realpath(__file__)))
        self.assertEqual(bot.files, os.path.dirname(os.path.realpath(__file__)) + '/files')
        self.assertNotEqual(bot.logging, None)
        self.assertNotEqual(bot.config, None)
        self.assertNotEqual(bot.behaviours, None)
        self.assertNotEqual(bot.admin, None)

    def test_handle_no_access(self):
        bot = self.build_mojo()
        bot.handle({'text': 'test', 'chat': {'id': 3}})
        bot.sendMessage.assert_called_with('1', 'Unauthorized access attempt by: 3')

    def test_handle(self):
        bot = self.build_mojo()
        bot.handle({'text': 'time', 'chat': {'id': 1}})
        # bot.sendMessage.assert_not_called_with('1', 'Unauthorized access attempt by: 3')
        bot.sendMessage.assert_called_with(1, datetime.datetime.now().strftime('%I:%M %p'), None, True)

    def test_handle_no_command(self):
        bot = self.build_mojo()
        bot.handle({'text': 'bob', 'chat': {'id': 1}})
        bot.sendMessage.assert_called_with(1, "I'm sorry I don't know what to say. How would you respond to that?", None, True)

    def build_bot(self):
        bot = Mock(return_value=456)
        bot.chat = Mock()
        bot.admin = 1
        bot.chat.respond = Mock(return_value='chat response')
        bot.do_command = Mock(return_value='command response')
        bot.config = Mock()
        bot.config.get = Mock(return_value='1,2')
        return bot

    def build_mojo(self):
        ConfigParser.ConfigParser = Mock()
        bot = mojo.Mojo()
        bot.sendMessage = Mock()
        bot.admin = '1'
        # bot.message = Mock()
        bot.config = Mock()
        bot.config.get = Mock(return_value='1,2')
        return bot


if __name__ == '__main__':
    unittest.main()
