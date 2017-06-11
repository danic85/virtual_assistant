#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import git
import os
from shutil import copyfile
import pip

from behaviours.behaviour import Behaviour

class General(Behaviour):

    routes = {
        '(what time is it|what is the time|time)\??$': 'time',
        '^(?:set )?config (.*)=(.*)$': 'config_set',
        'list commands|help|command list': 'command_list',
        'update': 'update_self',
        'shutdown pi': 'shutdown_self',
        'reboot pi': 'reboot_self',
        'morning others$': 'morning_others',
        'morning|good morning$': 'morning',
        'get log': 'get_log',
        'rotate log': 'rotate_log',
        'broadcast ([ a-z]+)': 'broadcast'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def config_set(self):
        return self.config.set(self.match.group(1), self.match.group(2))

    def config_get(self, key):
        return self.config.get(key)

    def morning(self):
        """
        Compile morning message for admin
        """
        self.act.chain_command('get closest countdowns')
        # response = self.chat.respond('good morning', self.admin) + '\n\n'
        # response += self.do_command('get closest countdowns') + '\n\n'
        # response += self.do_command('weather forecast') + '\n\n'
        # response += self.do_command('budget') + '\n\n'
        # response += self.do_command('thought of the day') + '\n\n'
        # response += self.do_command('did you know')
        return 'Good Morning!'

    def morning_others(self):
        """
        Compile morning message for non-admin users
        """
        self.act.user = self.config.get('Users').split(',')
        self.act.user.pop(0)
        self.act.chain_command('get closest countdowns')
        # response = self.chat.respond('good morning', self.admin) + '\n\n'
        # response += self.do_command('get closest countdowns') + '\n\n'
        # response += self.do_command('budget') + '\n\n'
        # response += self.do_command('weather forecast') + '\n\n'
        # response += self.do_command('thought of the day') + '\n\n'
        # response += self.do_command('did you know')
        return 'Good Morning!'

    def broadcast(self):
        """ Send message to all users """
        self.act.user = self.config.get('Users').split(',')
        return self.match.group(0)

    def command_list(self):
        """ List available commands """
        return "Check out the full list of commands:" \
               "\nhttps://github.com/danic85/mojo_home_bot/blob/master/README.md#commands"

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
        f = open(self.files + '/mojo_debug.log', 'r')
        self.sendDocument(self.act.user, f)
        return ''

    def rotate_log(self):
        copyfile(self.files + '/mojo_debug.log',
                 self.files + '/mojo_debug.log.' + str(datetime.datetime.today().weekday()))
        open(self.files + '/mojo_debug.log', 'w').close()
        return ''

    @staticmethod
    def time():
        """ Return current time in readable format """
        return datetime.datetime.now().strftime('%I:%M %p')

    @staticmethod
    def date_time():
        """ Return current date time in readable format """
        return datetime.datetime.now().strftime('%d-%m-%y %I:%M %p')