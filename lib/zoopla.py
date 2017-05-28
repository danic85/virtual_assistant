#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Powered by NewsAPI.org """

import requests
# import json
from decimal import Decimal


def zoopla_get(args):
    param_string = '&'.join(args)
    r = requests.get('http://api.zoopla.co.uk/api/v1/property_listings.js?' + param_string, verify=False)
    return r


def get_houses(self):
    api_key = self.config.get('Config', 'ZooplaAPI')

    args = [
            'latitude=' + '55.168039',
            'longitude=' + '-1.689599',
            'api_key=' + api_key,
            'minimum_beds=' + '2',
            'property_type=' + 'houses',
            'radius=' + '2',
            'maximum_price=' + '150000'
        ]

    json_str = zoopla_get(args)
    print json_str.status_code
    if json_str.status_code == 403:
        return 'Error: ' + json_str.headers['X-Error-Detail-Header']

    listings = json_str.json()['listing']
    # print json.dumps(listings, indent=4, sort_keys=True)

    response = []
    for listing in listings:
        price = '{:10,.2f}'.format(Decimal(listing['price']))
        r = [
            listing['displayable_address'],
            price,
            listing['details_url']
        ]
        response.append(' '.join(r))

    return '\n'.join(response)





