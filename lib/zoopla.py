#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Powered by NewsAPI.org """

import requests
# import json
from decimal import Decimal
import re, cgi


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
            'maximum_price=' + '150000',
            'page_size=' + '20',
            'order_by=' + 'age',
            'ordering=' + 'ascending',
            'listing_status=' + 'sale',
            'keywords=' + 'garden, parking'
        ]

    json_str = zoopla_get(args)
    print json_str.status_code
    if json_str.status_code == 403:
        return 'Error: ' + json_str.headers['X-Error-Detail-Header']

    listings = json_str.json()['listing']
    # print json.dumps(listings, indent=4, sort_keys=True)

    excluded_keywords = [
        'pegswood',
        'tenanted',
        'leasehold'
    ]

    response = []
    for listing in listings:
        if any(word in listing['description'].lower() for word in excluded_keywords) or any(word in listing['displayable_address'].lower() for word in excluded_keywords):
            continue
        price = '{:10,.2f}'.format(Decimal(listing['price']))

        # Remove HTML from description and shorten to first sentence
        tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
        no_tags = tag_re.sub('', listing['short_description'].split('.')[0] + '.')
        description = cgi.escape(no_tags).strip()
        if description.startswith("Summary"):
            description = description[7:]

        r = [
            listing['displayable_address'],
            '\n£'.decode("utf8") + price,
            '\n' + description,
            '\n' + listing['details_url'].split('?')[0]
        ]
        response.append(' '.join(r))

    return '\n\n'.join(response)





