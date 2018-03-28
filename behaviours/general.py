#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import git
import os
from shutil import copyfile
import pip
import lib.dt

from behaviours.behaviour import Behaviour

class General(Behaviour):

    routes = {
        '(what time is it|what is the time|time)\??$': 'time',
        '^(?:set )?config (.*)=(.*)$': 'config_set',
        'list commands|help|command list': 'command_list',
        'update': 'update_self',
        'emergency shutdown': 'shutdown_self',
        'emergency reboot': 'reboot_self',
        'morning|good morning$': 'morning',
        'get log': 'get_log',
        'rotate log': 'rotate_log',
        'broadcast ([ a-z]+)': 'broadcast',
        '^exit|quit$': 'exit'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.define_idle(self.rotate_log, 24, lib.dt.datetime_from_time(0, 0))
        # self.define_idle(self.morning, 24, lib.dt.datetime_from_time(8, 0))

    def config_set(self):
        return self.config.set(self.match.group(1), self.match.group(2))

    def config_get(self, key):
        return self.config.get(key)

    def morning(self):
        """
        Compile morning message for all
        """
        self.act.user = self.config.get('Users').split(',')
        self.act.chain_command('get closest countdowns')
        self.act.chain_command('detailed weather forecast')
        self.act.chain_command('check allowance')
        return 'Good Morning!'

    def broadcast(self):
        """ Send message to all users """
        self.act.user = self.config.get('Users').split(',')
        return self.match.group(0)

    def command_list(self):
        """ List available commands """
        return "Check out the full list of commands:" \
               "\nhttps://github.com/danic85/virtual_assistant/blob/master/README.md#commands"

    def update_self(self):
        """ Pull from github repo and restart if appropriate """
        # pull from git
        directory = self.dir
        g = git.cmd.Git(directory)
        g.fetch()

        response = g.pull()

        if 'Already up-to-date' not in response:
            # install requirements.txt and restart python app
            pip.main(['install', '-r', self.dir + '/requirements.txt'])
            os.execl(sys.executable, sys.executable, *sys.argv)

        return 'Updated'

    @staticmethod
    def shutdown_self():
        os.system("shutdown")
        return 'Shutting down...'

    @staticmethod
    def reboot_self():
        os.system("shutdown -r")
        return 'Rebooting...'

    def get_log(self):
        """ Send log file to user """
        self.act.respond_file(self.files + '/assistant_debug.log')
        self.act.respond_file(self.files + '/logfile.log')
        return ''

    def rotate_log(self):
        copyfile(self.files + '/assistant_debug.log',
                 self.files + '/assistant_debug.log.' + str(datetime.datetime.today().weekday()))
        open(self.files + '/assistant_debug.log', 'w').close()
        return ''

    @staticmethod
    def exit():
        quit()

    @staticmethod
    def time():
        """ Return current time in readable format """
        return datetime.datetime.now().strftime('%I:%M %p')

    @staticmethod
    def date_time():
        """ Return current date time in readable format """
        return datetime.datetime.now().strftime('%d-%m-%y %I:%M %p')
