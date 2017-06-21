#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import io
import requests
from datetime import datetime, timedelta
from behaviours.behaviour import Behaviour
from behaviours.expenses import Expenses
from lib import feeds

class Monzo(Behaviour):

    routes = {
        'get transactions': 'log_all_transactions',
        'get recent transactions': 'log_recent_transactions',
        '^add monzo token (.*) (.*) (.*)$': 'add_token'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'monzo'
        self.monzo_tokens = []
        filename = self.files + '/expenses/monzo-tokens.json'
        self.define_idle(self.log_recent_transactions, 0)
        if os.path.isfile(filename):
            with open(filename) as data_file:
                try:
                    self.monzo_tokens = json.load(data_file)
                except ValueError:
                    pass

    @staticmethod
    def authenticate(client_id, client_secret, redirect_uri, code):

        params = {"grant_type": "authorization_code",
                  "client_id": client_id,
                  "client_secret": client_secret,
                  "redirect_uri": redirect_uri,
                  "code": code}

        print(params)
        response = feeds.post_json("https://api.monzo.com/oauth2/token", params)
        print(json.dumps(response))
        if 'error' in response.keys():
            return response['message']

        monzo_token = {'access_token': response['access_token'],
                       'refresh_token': response['refresh_token'],
                       'client_id': client_id,
                       'client_secret': client_secret}
        return monzo_token

    def add_token(self):
        """ Add token via command 'add monzo token <auth_code> <client_id> <client_secret>'"""
        response = self.authenticate(self.match.group(2), self.match.group(3), 'http://localhost', self.match.group(1))
        if isinstance(response, str):
            return response
        self.monzo_tokens.append(response)
        self.write_tokens()
        return 'Token added'

    @staticmethod
    def __refresh_token(monzo_token):
        params = {"grant_type": "refresh_token",
                  "client_id": monzo_token['client_id'],
                  "client_secret": monzo_token['client_secret'],
                  "redirect_uri": 'http://localhost',
                  "refresh_token": monzo_token['refresh_token']}
        response = feeds.post_json("https://api.monzo.com/oauth2/token", params)

        if 'access_token' not in response:
            return None

        new_token = {'access_token': response['access_token'],
                     'refresh_token': response['refresh_token'],
                     'client_id': monzo_token['client_id'],
                     'client_secret': monzo_token['client_secret']}
        return new_token

    def write_tokens(self):
        filename = self.files + '/expenses/monzo-tokens.json'
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.monzo_tokens, ensure_ascii=False))

    @staticmethod
    def __is_authenticated(access_token):
        response = Monzo.__get(access_token, 'ping/whoami')
        if 'authenticated' not in response:
            return False
        return response['authenticated']

    @staticmethod
    def __get_accounts(access_token):
        """ return accounts list from given access token """
        return Monzo.__get(access_token, 'accounts')['accounts']

    @staticmethod
    def get_account_id(access_token, account_index):
        """ Return Account ID of given account index """
        return Monzo.__get_accounts(access_token)[account_index]['id']

    @staticmethod
    def get_balance(access_token, account_id):
        params = {"account_id": account_id}
        response = Monzo.__get(access_token, 'balance', params)
        return response['balance']

    @staticmethod
    def get_all_transactions(access_token, account_id):
        """ Return all transactions from a given account """
        params = {"account_id": account_id}
        return Monzo.__get(access_token, 'transactions', params)['transactions']

    @staticmethod
    def get_recent_transactions(access_token, account_id):
        """ Return transactions from a given account from the last 24 hours """
        one_day_ago = (datetime.today() - timedelta(days=1)).isoformat("T") + "Z"  # RFC 3339-encoded timestamp - 1 day
        params = {"account_id": account_id, "since": one_day_ago}
        return Monzo.__get(access_token, 'transactions', params)['transactions']

    @staticmethod
    def __get(access_token, endpoint, params=None):
        """ Trigger Get Request with given endpoint and access token. Include params if appropriate """
        full_endpoint = "https://api.monzo.com/" + endpoint
        headers = {"Authorization": "Bearer " + access_token}
        response = requests.get(full_endpoint, headers=headers, params=params).json()
        return response

    def log_recent_transactions(self):
        return self.__log_transactions(False)

    def log_all_transactions(self):
        return self.__log_transactions(True)

    def __log_transactions(self, log_all):
        """ Get monzo transactions for every account in each stored token """
        response = []
        count = 0
        changes = False
        expenses = Expenses(db=self.db, config=self.config, dir=self.dir, logging=self.logging)
        for monzo_token in self.monzo_tokens:
            if not self.__is_authenticated(monzo_token['access_token']):
                changes = True
                refreshed = self.__refresh_token(monzo_token)
                if refreshed and 'access_token' in refreshed:
                    monzo_token = refreshed
            if self.__is_authenticated(monzo_token['access_token']):
                for account in self.__get_accounts(monzo_token['access_token']):
                    if log_all:
                        transaction_list = self.get_all_transactions(monzo_token['access_token'], account['id'])
                    else:
                        transaction_list = self.get_recent_transactions(monzo_token['access_token'], account['id'])
                    for transaction in transaction_list:
                        if not transaction['include_in_spending']:
                            continue
                        if not expenses.transaction_exists(self, transaction['id']):

                            # Ignore previous months' transactions
                            today = datetime.now()
                            first = today.replace(day=1)
                            if datetime.strptime(transaction['created'], '%Y-%m-%dT%H:%M:%S.%fZ') < first:
                                continue

                            expense = [float(transaction['amount']) / 100, transaction['description'].split('  ')[0],
                                       transaction['id'], transaction['created']]
                            count = count + 1
                            response.append(expenses.write_to_file(self, expense))
            else:
                self.monzo_tokens.remove(monzo_token)
                changes = True
                response.append('Cannot refresh token with Monzo: ' + monzo_token['access_token'])
        if changes:
            self.write_tokens()
        if count > 5:
            return str(count) + ' expenses imported'
        return '\n'.join(response)
