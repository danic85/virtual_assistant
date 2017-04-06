import requests
import lib.expenses
from datetime import datetime, timedelta


def add_token(self):
    token = self.original_message.replace('add monzo token ', '')
    self.monzo_tokens.append(token)
    return 'Token added'


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


def get_transactions(access_token, account_id):
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


def get_new_transactions(self):
    """ Get monzo transactions for every account in each stored token """
    response = []
    for monzo_token in self.monzo_tokens:
        if is_authenticated(monzo_token):
            for account in get_accounts(monzo_token):
                for transaction in get_transactions(monzo_token, account['id']):
                    if not transaction['include_in_spending']:
                        continue
                    if not lib.expenses.transaction_exists(self, transaction['id']):
                        expense = [float(transaction['amount']) / 100, transaction['description'], transaction['id']]
                        response.append(lib.expenses.write_to_file(self, expense))
        else:
            self.monzo_tokens.remove(monzo_token)
            response.append('Not authenticated with Monzo: ' + monzo_token)
    return '\n'.join(response)
