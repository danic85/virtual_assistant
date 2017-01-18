#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import git
import pwd
import grp
import os
from os.path import getmtime

def morning(self):
      response = self.chat.respond('good morning', self.admin) + '\n\n'
      response += self.doCommand('get countdowns') + '\n\n'
      response += self.doCommand('weather') + '\n\n'
      response += self.doCommand('budget') + '\n\n'
      response += self.doCommand('shower thought') + '\n\n'
      response += self.doCommand('riddle')
      return response

def morning_others(self):
      self.user = self.config.get('Config','Users').split(',')
      self.user.pop(0)
      response = self.chat.respond('good morning', self.admin) + '\n\n'
      response += self.doCommand('get countdowns') + '\n\n'
      response += self.doCommand('budget') + '\n\n'
      response += self.doCommand('weather') + '\n\n'
      response += self.doCommand('shower thought')
      return response

# Send message to all users
def broadcast(self):
    self.user = self.config.get('Config','Users').split(',')
    return self.command.replace('broadcast ', '', 1)

def time(self):
    return datetime.datetime.now().strftime('%I:%M %p')

def date_time(self):
    return datetime.datetime.now().strftime('%d-%m-%y %I:%M %p')
    
def set_countdown(self):
    cmd = self.command.replace('countdown ', '')
    with open(self.files + '/countdowns.txt', 'a') as f:
        f.write(cmd+'\n')
    return get_countdowns(self)

def get_countdowns(self):
    countdowns = ''
    with open(self.files + '/countdowns.txt', 'r') as f:
        for line in f:
            cmd = line.strip().split(' ', 1)
            date = cmd[0].split('-')
            event = cmd[1]
            countdowns += countdown(self, int(date[2]), int(date[1]), int(date[0]), event) + '\n'
    return countdowns.strip()

def countdown(self, year, month, day, event):
    delta = datetime.datetime(year, month, day) - datetime.datetime.now()
    days = delta.days+1
    if (days < 0):
        return ''
    if (days == 0):
        return 'Today is ' + event + '!'
    return str(days) + ' days until ' + event

def command_list(self):
    response = "Available commands:\n"
    for key, val in self.commandList:
        response += key + "\n"
    return response
    
def update_self(self, f):
    return 'Feature disabled' # Feature is temperamental, awaiting refactor
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
    f = open(self.dir + '/mojo_debug.log', 'r')
    self.sendDocument(self.user, f)
    return ''