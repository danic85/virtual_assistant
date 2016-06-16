#!/usr/bin/env python
# -*- coding: utf-8 -*-

#expenses
import csv, datetime

def expenses_remaining(self):
    remaining = 0.0;
    with open(self.dir + '/' + self.config.get('Config','ExpensesFile'), 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            remaining += float(row[1].strip())
    return 'There is £' + str(format(remaining, '.2f')) + ' left this month.';

def expenses_add(self):
    expense = self.command.split(' ', 1)
    with open(self.dir + '/' + self.config.get('Config','ExpensesFile'), 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([expense[1], float(expense[0].strip()) * -1, datetime.datetime.now(), self.user])
    self.user = self.config.get('Config','Users').split(',')
    return 'Logged expense: ' + str(self.command) + "\n" + self.expenses_remaining()