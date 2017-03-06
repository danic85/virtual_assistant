#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import git
import pwd
import grp
import os


def morning(self):
    """
    Compile morning message for admin
    :param self: Mojo()
    :return: response string
    """
    response = self.chat.respond('good morning', self.admin) + '\n\n'
    response += self.do_command('get countdowns') + '\n\n'
    response += self.do_command('weather') + '\n\n'
    response += self.do_command('budget') + '\n\n'
    response += self.do_command('thought of the day') + '\n\n'
    response += self.do_command('did you know')
    return response


def morning_others(self):
    """
    Compile morning message for non-admin users
    :param self: Mojo()
    :return: response string
    """
    self.user = self.config.get('Config', 'Users').split(',')
    self.user.pop(0)
    response = self.chat.respond('good morning', self.admin) + '\n\n'
    response += self.do_command('get countdowns') + '\n\n'
    response += self.do_command('budget') + '\n\n'
    response += self.do_command('weather') + '\n\n'
    response += self.do_command('thought of the day') + '\n\n'
    response += self.do_command('did you know')
    return response


def broadcast(self):
    """ Send message to all users """
    self.user = self.config.get('Config', 'Users').split(',')
    return self.command.replace('broadcast ', '', 1)


def time(self):
    """ Return current time in readable format """
    return datetime.datetime.now().strftime('%I:%M %p')


def date_time(self):
    """ Return current date time in readable format """
    return datetime.datetime.now().strftime('%d-%m-%y %I:%M %p')


def set_countdown(self):
    """ Add countdown to countdowns list """
    cmd = self.command.replace('countdown ', '')
    with open(self.files + '/countdowns.txt', 'a') as f:
        f.write(cmd + '\n')
    return get_countdowns(self)


def get_countdowns(self):
    """ Get all countdowns from list """
    countdowns = ''
    with open(self.files + '/countdowns.txt', 'r') as f:
        for line in f:
            cmd = line.strip().split(' ', 1)
            date = cmd[0].split('-')
            event = cmd[1]
            countdowns += countdown(self, int(date[2]), int(date[1]), int(date[0]), event) + '\n'
    return countdowns.strip()


def countdown(self, year, month, day, event):
    """ Return string of countdown """
    delta = datetime.datetime(year, month, day) - datetime.datetime.now()
    days = delta.days + 1
    if (days < 0):
        return ''
    if (days == 0):
        return 'Today is ' + event + '!'
    return str(days) + ' days until ' + event


def command_list(self):
    """ List available commands """
    response = "Available commands:\n"
    for key, val in self.commandList:
        response += key + "\n"
    return response


def update_self(self, f):
    """ Pull from github repo and restart if appropriate """
    return 'Feature disabled'  # Feature is temperamental, awaiting refactor
    # pull from git
    directory = self.dir
    g = git.cmd.Git(directory)
    g.pull()

    # Update owner of files to prevent permission issues
    uid = pwd.getpwnam("pi").pw_uid
    gid = grp.getgrnam("pi").gr_gid
    for root, dirs, files in os.walk(directory):
        for momo in dirs:
            os.chown(os.path.join(root, momo), uid, gid)
        for momo in files:
            os.chown(os.path.join(root, momo), uid, gid)

    # Check if the file has changed.
    # If so, restart the application.
    if os.path.getmtime(f) > self.last_mtime:
        # Restart the application (os.execv() does not return).
        os.execv(f, sys.argv)

    return 'Updated to version: ' + str(self.last_mtime)


def get_log(self):
    """ Send log file to user """
    f = open(self.dir + '/mojo_debug.log', 'r')
    self.sendDocument(self.user, f)
    return ''
