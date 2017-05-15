import os
import json
import io
import requests
import lib.expenses
from datetime import datetime, timedelta, date


def init(self):
    filename = self.files + '/expenses/monzo-tokens.json'
    if os.path.isfile(filename):
        with open(filename) as data_file:
            try:
                self.monzo_tokens = json.load(data_file)
            except ValueError:
                pass


def authenticate(client_id, client_secret, redirect_uri, code):

    params = {"grant_type": "authorization_code",
              "client_id": client_id,
              "client_secret": client_secret,
              "redirect_uri": redirect_uri,
              "code": code}
    response = requests.post("https://api.monzo.com/oauth2/token", data=params).json()
    print response
    if 'error' in response.keys():
        return response['message']

    monzo_token = {'access_token': response['access_token'],
                   'refresh_token': response['refresh_token'],
                   'client_id': client_id,
                   'client_secret': client_secret}
    return monzo_token


def add_token(self):
    """ Add token via command 'add monzo token <auth_code> <client_id> <client_secret>'"""
    token = self.original_message.replace('add monzo token ', '')
    input = token.split(' ')
    print input
    response = authenticate(input[1], input[2], 'http://localhost', input[0])
    if isinstance(response, basestring):
        return response
    self.monzo_tokens.append(response)
    write_tokens(self)
    return 'Token added'


def refresh_token(monzo_token):
    params = {"grant_type": "refresh_token",
              "client_id": monzo_token['client_id'],
              "client_secret": monzo_token['client_secret'],
              "redirect_uri": 'http://localhost',
              "refresh_token": monzo_token['refresh_token']}
    response = requests.post("https://api.monzo.com/oauth2/token", data=params).json()
    new_token = {'access_token': response['access_token'],
                   'refresh_token': response['refresh_token'],
                   'client_id': monzo_token['client_id'],
                   'client_secret': monzo_token['client_secret']}
    return new_token


def write_tokens(self):
    filename = self.files + '/expenses/monzo-tokens.json'
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(self.monzo_tokens, ensure_ascii=False))


def is_authenticated(access_token):
    response = monzo_request_get(access_token, 'ping/whoami')
    if 'authenticated' not in response:
        return False
    return response['authenticated']


def get_accounts(access_token):
    """ return accounts list from given access token """
    return monzo_request_get(access_token, 'accounts')['accounts']


def get_account_id(access_token, account_index):
    """ Return Account ID of given account index """
    return get_accounts(access_token)[account_index]['id']


def get_balance(access_token, account_id):
    params = {"account_id": account_id}
    response = monzo_request_get(access_token, 'balance', params)
    return response['balance']


def get_all_transactions(access_token, account_id):
    """ Return all transactions from a given account """
    params = {"account_id": account_id}
    return monzo_request_get(access_token, 'transactions', params)['transactions']


def get_recent_transactions(access_token, account_id):
    """ Return transactions from a given account from the last 24 hours """
    one_day_ago = (datetime.today() - timedelta(days=1)).isoformat("T") + "Z"  # RFC 3339-encoded timestamp - 1 day
    params = {"account_id": account_id, "since": one_day_ago}
    return monzo_request_get(access_token, 'transactions', params)['transactions']


def monzo_request_get(access_token, endpoint, params = None):
    """ Trigger Get Request with given endpoint and access token. Include params if appropriate """
    full_endpoint = "https://api.monzo.com/" + endpoint
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(full_endpoint, headers=headers, params=params).json()
    return response


def log_recent_transactions(self):
    return log_transactions(self, False)


def log_all_transactions(self):
    return log_transactions(self, True)


def log_transactions(self, all):
    """ Get monzo transactions for every account in each stored token """
    response = []
    count = 0
    changes = False
    for monzo_token in self.monzo_tokens:
        if not is_authenticated(monzo_token['access_token']):
            changes = True
            monzo_token = refresh_token(monzo_token)
        if is_authenticated(monzo_token['access_token']):
            for account in get_accounts(monzo_token['access_token']):
                if all:
                    transaction_list = get_all_transactions(monzo_token['access_token'], account['id'])
                else:
                    transaction_list = get_recent_transactions(monzo_token['access_token'], account['id'])
                for transaction in transaction_list:
                    if not transaction['include_in_spending']:
                        continue
                    if not lib.expenses.transaction_exists(self, transaction['id']):

                        # Ignore previous months' transactions
                        today = datetime.now()
                        first = today.replace(day=1)
                        if datetime.strptime(transaction['created'], '%Y-%m-%dT%H:%M:%S.%fZ') < first:
                            continue

                        expense = [float(transaction['amount']) / 100, transaction['description'].split('  ')[0], transaction['id'], transaction['created']]
                        count = count+1
                        response.append(lib.expenses.write_to_file(self, expense))
        else:
            self.monzo_tokens.remove(monzo_token)
            changes = True
            response.append('Cannot refresh token with Monzo: ' + monzo_token['access_token'])
    if changes:
        write_tokens(self)
    if count > 5:
        return str(count) + ' expenses imported'
    return '\n'.join(response)
