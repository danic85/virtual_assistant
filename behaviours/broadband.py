#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behaviours.behaviour import Behaviour
import speedtest


class Broadband(Behaviour):

    routes = {
        'speed test': 'report_test'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        #self.define_idle(self.low_speed_check, 0)

    def report_test(self):
        results = self.run_test()
        return 'Speed test: Upload = ' + \
               self.bites_to_mbites(results.upload) + \
               'Mb/s. Download = ' + self.bites_to_mbites(results.download) + \
               'Mb/s'

    def run_test(self):
        servers = []
        # If you want to test against a specific server
        # servers = [1234]

        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download()
        s.upload()
        # s.results.share()
        # results_dict = s.results.dict()
        return s.results

    @staticmethod
    def bites_to_mbites(bites):
        return str(round(bites / 1000000, 1))

    def low_speed_check(self):
        results = self.run_test()
        if float(self.bites_to_mbites(results.upload)) < 1 or float(self.bites_to_mbites(results.download)) < 1:
            return 'Low broadband speed detected: Upload = ' + \
               self.bites_to_mbites(results.upload) + \
               'Mb/s. Download = ' + self.bites_to_mbites(results.download) + \
               'Mb/s'
        return ''
