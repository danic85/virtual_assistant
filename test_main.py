#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime, os, unittest
import main
from mock import Mock, call, patch
from freezegun import freeze_time


class TestMainMethods(unittest.TestCase):

    def test_execute_command(self):
        bot = self.build_bot()
        bot.handle = Mock()
        main.execute_bot_command(bot, 'test')
        bot.handle.assert_called_with({'text': 'test', 'chat': {'id': 1}})

    @freeze_time("2017-01-01")
    def test_execute_command_monthly_first(self):
        bot = self.build_bot()
        bot.handle = Mock()
        main.execute_bot_command_monthly(bot, 'test')
        bot.handle.assert_called_with({'text': 'test', 'chat': {'id': 1}})

    @freeze_time("2017-01-02")
    def test_execute_command_monthly_not_first(self):
        bot = self.build_bot()
        bot.handle = Mock()
        main.execute_bot_command_monthly(bot, 'test')
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


if __name__ == '__main__':
    unittest.main()
