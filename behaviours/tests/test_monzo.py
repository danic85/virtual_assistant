#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import Mock, call, patch, mock_open
import datetime
from lib.interaction import Interaction
from behaviours import monzo
import re, os
from freezegun import freeze_time
import json
from lib import feeds

class TestMonzoMethods(unittest.TestCase):

    def test_routes(self):
        b = monzo.Monzo(db=None, config={}, dir='')
        act = Interaction()
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        b.log_expense = Mock()
        b.log_all_transactions = Mock()
        b.log_recent_transactions = Mock()
        b.add_token = Mock()

        response = b.handle(act)
        self.assertEqual(response, None)

        act.command = {'text': 'get transactions'}
        b.handle(act)
        b.log_all_transactions.assert_called_once()

        act.command = {'text': 'get recent transactions'}
        b.handle(act)
        b.log_recent_transactions.assert_called_once()

        act.command = {'text': 'add monzo token auth_code client_id client_secret'}
        b.handle(act)
        b.log_expense.add_token()
        self.assertEqual(b.match.group(1), 'auth_code')
        self.assertEqual(b.match.group(2), 'client_id')
        self.assertEqual(b.match.group(3), 'client_secret')

    def test_authenticate_failure(self):
        b = monzo.Monzo(db=None, config={}, dir='')
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        data = {"message": "Invalid client credentials", "error_description": "Invalid client credentials", "error": "invalid_client"}
        feeds.post_json = Mock(return_value=data)

        response = b.authenticate('client_id', 'client_secret', 'redirect_uri', 'code')

        self.assertEqual(response, 'Invalid client credentials')


    def test_authenticate(self):
        auth_code = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaSI6Im9hdXRoY2xpZW50XzAwMDA5TEtjQ1JONFhFUkpRckpDWFIiLCJleHAiOjE0OTcxODg0NTksImlhdCI6MTQ5NzE4NDg1OSwianRpIjoiYXV0aGNvZGVfMDAwMDlMS2RIUG5CdnFOVndEU2dneiIsInVpIjoidXNlcl8wMDAwOUl2WWwzOWZER2FSUVBwTFh0IiwidiI6IjIifQ.Rf1p0GXQSbU8VdvVDpnbVmG-vsHqpzMA-NnKh3iBYMQ'
        client_id = 'oauthclient_00009LKcCRN4XERJQrJCXR'
        client_secret = 'E0sBuDCz8lf3TQDP3tHzOPTKGvLRh/J93vo5I57QjTcZnaecoFB7JuADBH9p4NnllrW2qQTNpEdsKd1qgp4v'

        b = monzo.Monzo(db=None, config={}, dir='')
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        data = {"user_id": "user_00009IvYl39fDGaRQPpLXt", "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaSI6Im9hdXRoY2xpZW50XzAwMDA5TEtjQ1JONFhFUkpRckpDWFIiLCJleHAiOjE0OTcyMDY1NDQsImlhdCI6MTQ5NzE4NDk0NCwianRpIjoidG9rXzAwMDA5TEtkUEc4RmpUcXRCbUJSZFIiLCJ1aSI6InVzZXJfMDAwMDlJdllsMzlmREdhUlFQcExYdCIsInYiOiIyIn0.sIlSx1hp1mcXw5NXEMyISmlRTRSuluuKOu-UKqt7aoA", "expires_in": 21599, "token_type": "Bearer", "client_id": "oauthclient_00009LKcCRN4XERJQrJCXR", "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaSI6InRva18wMDAwOUxLZFBHOEZqVHF0Qm1CUmRSIiwiY2kiOiJvYXV0aGNsaWVudF8wMDAwOUxLY0NSTjRYRVJKUXJKQ1hSIiwiaWF0IjoxNDk3MTg0OTQ0LCJ1aSI6InVzZXJfMDAwMDlJdllsMzlmREdhUlFQcExYdCIsInYiOiIyIn0.hR5CheZKJHIXai088se3TXx-OsYPiHjDYxli5DogW0Y"}
        feeds.post_json = Mock(return_value=data)

        response = b.authenticate(client_id, client_secret, 'http://localhost', auth_code)

        self.assertEqual(response, {'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaSI6Im9hdXRoY2xpZW50XzAwMDA5TEtjQ1JONFhFUkpRckpDWFIiLCJleHAiOjE0OTcyMDY1NDQsImlhdCI6MTQ5NzE4NDk0NCwianRpIjoidG9rXzAwMDA5TEtkUEc4RmpUcXRCbUJSZFIiLCJ1aSI6InVzZXJfMDAwMDlJdllsMzlmREdhUlFQcExYdCIsInYiOiIyIn0.sIlSx1hp1mcXw5NXEMyISmlRTRSuluuKOu-UKqt7aoA', 'client_secret': 'E0sBuDCz8lf3TQDP3tHzOPTKGvLRh/J93vo5I57QjTcZnaecoFB7JuADBH9p4NnllrW2qQTNpEdsKd1qgp4v', 'client_id': 'oauthclient_00009LKcCRN4XERJQrJCXR', 'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaSI6InRva18wMDAwOUxLZFBHOEZqVHF0Qm1CUmRSIiwiY2kiOiJvYXV0aGNsaWVudF8wMDAwOUxLY0NSTjRYRVJKUXJKQ1hSIiwiaWF0IjoxNDk3MTg0OTQ0LCJ1aSI6InVzZXJfMDAwMDlJdllsMzlmREdhUlFQcExYdCIsInYiOiIyIn0.hR5CheZKJHIXai088se3TXx-OsYPiHjDYxli5DogW0Y'})

    def test_add_token(self):
        b = monzo.Monzo(db=None, config={}, dir='')
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        data = {"user_id": "user_00009IvYl39fDGaRQPpLXt", "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaSI6Im9hdXRoY2xpZW50XzAwMDA5TEtjQ1JONFhFUkpRckpDWFIiLCJleHAiOjE0OTcyMDY1NDQsImlhdCI6MTQ5NzE4NDk0NCwianRpIjoidG9rXzAwMDA5TEtkUEc4RmpUcXRCbUJSZFIiLCJ1aSI6InVzZXJfMDAwMDlJdllsMzlmREdhUlFQcExYdCIsInYiOiIyIn0.sIlSx1hp1mcXw5NXEMyISmlRTRSuluuKOu-UKqt7aoA", "expires_in": 21599, "token_type": "Bearer", "client_id": "oauthclient_00009LKcCRN4XERJQrJCXR", "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaSI6InRva18wMDAwOUxLZFBHOEZqVHF0Qm1CUmRSIiwiY2kiOiJvYXV0aGNsaWVudF8wMDAwOUxLY0NSTjRYRVJKUXJKQ1hSIiwiaWF0IjoxNDk3MTg0OTQ0LCJ1aSI6InVzZXJfMDAwMDlJdllsMzlmREdhUlFQcExYdCIsInYiOiIyIn0.hR5CheZKJHIXai088se3TXx-OsYPiHjDYxli5DogW0Y"}
        feeds.post_json = Mock(return_value=data)

        b.match = re.search('^add monzo token (.*) (.*) (.*)$', 'add monzo token auth_code client_id client_secret', re.IGNORECASE)
        b.write_tokens = Mock()
        assert len(b.monzo_tokens) == 0
        response = b.add_token()
        self.assertEqual(response, 'Token added')
        b.write_tokens.assert_called_once()
        assert len(b.monzo_tokens) > 0
        print('Tokens')
        print(b.monzo_tokens)

    # def test_log_recent_transactions(self):
    #     b = monzo.Monzo(db=None, config={}, dir='')
    #     b.config = Mock()
    #     b.config.get = Mock(return_value='1234,12345')
    #     b.logging = Mock()
    #     b.logging.info = Mock(return_value=True)
    #
    #     self.assertEqual(b.log_recent_transactions(), '')




