#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
from bs4 import BeautifulSoup


def check(self):
    url = 'https://www.dslchecker.bt.com/adsl/adslchecker.TelephoneNumberOutput'
    r = requests.post(url, data={
        'TelNo': self.config.get('Config', 'FibreTel'),
        'SP_NAME': 'a%20service%20provider',
        'VERSION': '45',
        'MS': 'E',
        'CAP': 'no',
        'AEA': "Y"
    })
    soup = BeautifulSoup(r.content, 'html.parser')

    found_something = False

    trs = soup.findAll("tr")
    if len(trs) == 0:
        return 'Could not connect to fibre checker website'
    for tr in trs:
        tds = tr.findAll("td")
        match = False
        for td in tds:
            if match and td.text != '--' and not is_number(td.text) and td.text != 'Yes':
                if td.text != 'Waiting list':
                    print 'Change detected'
                    return 'It looks like the status of fibre broadband has changed! http://dslchecker.bt.com'
            if td.text in ("FTTC Range A (Clean)", "FTTC Range B (Impacted)", "VDSL Range A (Clean)", "VDSL Range B (Impacted)"):
                match = True
                found_something = True

    if not found_something:
        return 'Could not parse fibre checker website'

    print ('executed')
    return 'No change to fibre broadband availability.' if random.randint(0, 3) > 2 else ''


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
