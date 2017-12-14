#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from decimal import Decimal
import re
import cgi
from behaviours.behaviour import Behaviour
import lib.feeds
from fuzzywuzzy import fuzz

class Salesforce(Behaviour):

    routes = {
        'salesforce jobs': 'get_jobs',
        'all salesforce jobs': 'get_all_jobs'
    }

    endpoints = {
        'search': 'http://salesforce.careermount.com/candidate/job_search/quick/results?location=UK%2B-%2BRemote&rss'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'properties'
        self.define_idle(self.get_jobs, 1)  # fetch new jobs every hour

    def get_all_jobs(self):
        return self.get_jobs(False)

    def get_jobs(self, only_new=True):

        jobs = lib.feeds.get_rss(self.endpoints['search'])

        title_matches = [
            'Lead Member of Technical Staff',
            'Lead Software Engineer',
            'Manager, Software Development',
            'Software Engineering Manager',
            'Program Manager'
        ]

        matching_entries = []

        for entry in jobs['entries']:
            for title in title_matches:
                # print(entry['title'] + ' - ' + str(fuzz.partial_ratio(title, entry['title'])))
                if fuzz.partial_ratio(title, entry['title']) > 70:
                    matching_entries.append(entry)

        response = []
        if len(matching_entries) > 0:

            for entry in matching_entries:
                r = [
                    entry['title'],
                    '\n' + entry['link']
                ]
                if self.__save_if_new(entry) or only_new is False:
                    response.append(' '.join(r))

        self.__remove_old(jobs['entries'])
        return '\n\n'.join(response)

    def __save_if_new(self, entry):
        if self.db.find('salesforce_jobs', {'id': entry['id']}).count() > 0:
            return False

        self.db.insert('salesforce_jobs', {'id': entry['id']})
        return True

    def __remove_old(self, entries):
        for p in self.db.find('salesforce_jobs'):
            found = False
            for entry in entries:
                if entry['id'] == p['id']:
                    found = True
            if not found:
                self.db.delete(p)