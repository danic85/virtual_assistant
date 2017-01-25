#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime, os, unittest
import mojo, aiml, ConfigParser
from mock import Mock, call, patch
from freezegun import freeze_time


class TestMojoMethods(unittest.TestCase):
    def test_mojo(self):
        aiml.Kernel = Mock()
        ConfigParser.ConfigParser = Mock()
        bot = mojo.Mojo()
        self.assertEqual(bot.dir, os.path.dirname(os.path.realpath(__file__)))
        self.assertEqual(bot.files, os.path.dirname(os.path.realpath(__file__)) + '/files')
        self.assertNotEqual(bot.logging, None)
        self.assertNotEqual(bot.config, None)
        self.assertNotEqual(bot.commandList, None)
        self.assertEqual(bot.user, False)
        self.assertEqual(bot.command, False)
        self.assertNotEqual(bot.admin, None)
        self.assertNotEqual(bot.adminName, None)
        self.assertNotEqual(bot.chat, None)
        self.assertNotEqual(bot.last_mtime, None)

    def test_handle_no_access(self):
        bot = self.build_mojo()
        bot.handle({'text': 'test', 'chat': {'id': 3}})
        bot.admin_message.assert_called_with('Unauthorized access attempt by: 3')

    def test_handle(self):
        bot = self.build_mojo()
        bot.handle({'text': 'time', 'chat': {'id': 1}})
        bot.admin_message.assert_not_called()
        bot.do_command.assert_called_with('time')
        bot.chat.respond.assert_not_called()
        self.assertNotEqual(bot.message, None)
        self.assertEqual(bot.user, False)
        self.assertEqual(bot.command, False)

    def test_handle_no_command(self):
        bot = self.build_mojo()
        bot.do_command = Mock(return_value=False)
        bot.handle({'text': 'bob', 'chat': {'id': 1}})
        bot.admin_message.assert_not_called()
        bot.do_command.assert_called_with('bob')
        bot.chat.respond.assert_called_with('bob', bot.admin)
        self.assertNotEqual(bot.message, None)
        self.assertEqual(bot.user, False)
        self.assertEqual(bot.command, False)

    def test_execute_command(self):
        bot = self.build_bot()
        bot.handle = Mock()
        mojo.execute_bot_command(bot, 'test')
        bot.handle.assert_called_with({'text': 'test', 'chat': {'id': 1}})

    @freeze_time("2017-01-01")
    def test_execute_command_monthly_first(self):
        bot = self.build_bot()
        bot.handle = Mock()
        mojo.execute_bot_command_monthly(bot, 'test')
        bot.handle.assert_called_with({'text': 'test', 'chat': {'id': 1}})

    @freeze_time("2017-01-02")
    def test_execute_command_monthly_not_first(self):
        bot = self.build_bot()
        bot.handle = Mock()
        mojo.execute_bot_command_monthly(bot, 'test')
        bot.handle.assert_not_called()

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
        aiml.Kernel = Mock()
        ConfigParser.ConfigParser = Mock()
        bot = mojo.Mojo()
        bot.do_command = Mock(return_value='Test')
        bot.admin_message = Mock()
        bot.chat = Mock()
        bot.chat.respond = Mock(return_value='chat response')
        bot.message = Mock()
        bot.config = Mock()
        bot.config.get = Mock(return_value='1,2')
        return bot


if __name__ == '__main__':
    unittest.main()
