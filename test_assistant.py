#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime, os, unittest
import assistant, sys, lib
from mock import Mock, call, patch, mock_open
from behaviours.general import General
from lib import config


class TestAssistantMethods(unittest.TestCase):
    def test_assistant(self):
        with patch('os.walk') as mockwalk:
            mockwalk.return_value = [
                ('/foo', ('bar',), ('baz',)),
            ]
            config.Config = Mock()
            config.Config.get = Mock(return_value=1234)
            bot = assistant.Assistant()
            self.assertEqual(bot.dir, os.path.dirname(os.path.realpath(__file__)))
            self.assertEqual(bot.files, os.path.dirname(os.path.realpath(__file__)) + '/files')
            self.assertNotEqual(bot.logging, None)
            self.assertNotEqual(bot.config, None)
            self.assertNotEqual(bot.behaviours, None)

    # def test_handle_no_access(self):
    #     bot = self.build_assistant()
    #     bot.handle({'text': 'test', 'chat': {'id': 3}})
    #     bot.responder.admin_message.assert_called_with('Unauthorized access attempt by: 3')

    def test_handle(self):
        bot = self.build_assistant()
        bot.behaviours[0] = [General(db=None, config=bot.config, dir='', logging=bot.logging)]
        bot.handle({'text': 'time', 'chat': {'id': 1}})
        bot.responder.sendMessage.assert_called_with(1, datetime.datetime.now().strftime('%I:%M %p'), None, True)

    def test_handle_console(self):
        bot = self.build_assistant()
        bot.mode = 'console'
        bot.handle({'text': 'time', 'chat': {'id': 1}})
        bot.responder.sendMessage.assert_called_with(1, "I'm sorry I don't know what to say", None, True)

    # def test_handle_voice(self):
    #     mocked_open = mock_open(read_data='file contents\nas needed\n')
    #     with patch('assistant.open', mocked_open, create=True):
    #             bot = self.build_assistant()
    #             lib.speech = Mock()
    #             bot.sendAudio = Mock()
    #             lib.speech.get_message = Mock(return_value='audio message')
    #             bot.handle({'voice': 'something', 'chat': {'id': 1}})
    #             lib.speech.get_message.assert_called_once()
    #             bot.responder.sendMessage.assert_not_called()
    #             bot.responder.sendAudio.assert_called_once()

    def test_handle_chain_commands(self):
        bot = self.build_assistant()

        mock_behaviour = Mock()
        mock_behaviour.handle = Mock(return_value='Test')
        mock_behaviour.handle.side_effect = self.chain_command
        bot.behaviours = {0: [mock_behaviour]}

        bot.handle({'text': 'time', 'chat': {'id': 1}})
        self.assertEqual(bot.responder.sendMessage.call_count, 2)

    def chain_command(self, act):
        if act.command['text'] != 'chain':
            act.response = [{'text': 'first', 'user': act.user},
                            {'command': {'text': 'chain'}, 'user': act.user}]

    def test_handle_no_behaviours(self):
        bot = self.build_assistant()
        bot.behaviours = {}
        bot.handle({'text': 'time', 'chat': {'id': 1}})
        bot.responder.sendMessage.assert_called_with(1, "I'm sorry I don't know what to say", None, True)

    def test_handle_behaviour_exception(self):
        bot = self.build_assistant()
        mock_behaviour = Mock()
        mock_behaviour.handle = Mock(return_value='Test')
        mock_behaviour.handle.side_effect = Mock(side_effect=Exception('Test'))
        bot.behaviours = {0: [mock_behaviour]}
        bot.handle({'text': 'time', 'chat': {'id': 1}})
        bot.responder.sendMessage.assert_called_with(1, "An exception of type Exception occurred with the message 'Test'. Arguments:\n('Test',)", None, True)

    def test_handle_no_command(self):
        bot = self.build_assistant()
        bot.handle({'text': 'bob', 'chat': {'id': 1}})
        bot.responder.sendMessage.assert_called_with(1, "I'm sorry I don't know what to say", None, True)

    def build_bot(self):
        bot = Mock(return_value=456)
        bot.chat = Mock()
        bot.admin = 1
        bot.chat.respond = Mock(return_value='chat response')
        bot.do_command = Mock(return_value='command response')
        bot.config = Mock()
        bot.config.get = Mock(return_value='1,2')
        return bot

    def build_assistant(self):
        Database = Mock()

        # Do not load any behaviours so we are testing those methods separately
        with patch('os.walk') as mockwalk:
            mockwalk.return_value = [
                ('/foo', ('bar',), ('baz',)),
            ]
            bot = assistant.Assistant()
            bot.responder = Mock()
            bot.responder.get_text = Mock()
            bot.responder.get_text.side_effect = self.mock_get_text
            bot.responder.sendMessage = Mock()
            bot.admin = '1'
            bot.config = Mock()
            bot.config.get = Mock(return_value='1,2')
            bot.config.get_or_request = Mock(return_value='1,2')
            logging = Mock()
            logging.info = Mock()
        return bot

    def mock_get_text(self, msg):
        return msg['text']

if __name__ == '__main__':
    unittest.main()
