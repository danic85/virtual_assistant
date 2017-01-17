#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
import os

def convert_usd(self):
    convert(self, 'USD', self.command.replace('convert ',''), self.config.get('Config', 'OpenExchangeRatesKey'))
# Convert currency into GBP (as long as it's USD!)    
def convert(self, currency, amount, key):
    endpoint = 'https://openexchangerates.org/api/latest.json?app_id=' + key
    gbp = json.load(urllib2.urlopen(endpoint))['rates']['GBP']
    conversion = float(amount) * float(gbp)
    #os.remove(key+'.json')
    return conversion