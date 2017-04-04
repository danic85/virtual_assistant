import requests

def is_authenticated(access_token):
    response = monzo_request_get(access_token, 'ping/whoami')
    return response['authenticated']


def get_accounts(access_token):
    return monzo_request_get(access_token, 'accounts')['accounts']


def get_account_id(access_token, account_index):
    return get_accounts(access_token)[account_index]['id']


def get_balance(access_token, account_id):
    params = {"account_id": account_id}
    response = monzo_request_get(access_token, 'balance', params)
    return response['balance']


def get_transactions(access_token, account_id):
    params = {"account_id": account_id}
    return monzo_request_get(access_token, 'transactions', params)['transactions']


def monzo_request_get(access_token, endpoint, params = None):
    full_endpoint = "https://api.monzo.com/" + endpoint
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(full_endpoint, headers=headers, params=params).json()
    return response


def demo():
    token = ''  # get access token from https://developers.monzo.com/api/playground
    print is_authenticated(token)
    print get_accounts(token)
    acct = get_account_id(token, 0)
    print acct
    print get_balance(token, acct)
    print get_transactions(token, acct)
