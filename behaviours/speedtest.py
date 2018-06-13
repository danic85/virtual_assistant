#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behaviours.behaviour import Behaviour
import speedtest


class SpeedTest(Behaviour):

    routes = {
        'speed test': 'run_test'
    }

    def run_test(self):
        servers = []
        # If you want to test against a specific server
        # servers = [1234]

        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download()
        s.upload()
        #s.results.share()
        #results_dict = s.results.dict()

        return 'Speed test: Upload = ' + round(s.results.upload / 1000000, 1) + 'Mb/s. Download = ' + round(s.results.download / 1000000, 1) + 'Mb/s'
