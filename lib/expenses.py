#!/usr/bin/env python
# -*- coding: utf-8 -*-

#expenses
import csv, datetime
import lib.currency

def expenses_remaining(self):
    remaining = 0.0;
    with open(self.dir + '/' + self.config.get('Config','ExpensesFile'), 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            remaining += float(row[1].strip())
    response = 'There is £' + str(format(remaining, '.2f')) + ' left this month.'
    return response.decode("utf8");

def expenses_add(self):
    expense = self.command.split(' ', 1)
    if expense[0].find("$") == 0:
        expense[0] = str(lib.currency.convert(self, 'USD', expense[0].replace('$',''), self.config.get('Config', 'OpenExchangeRatesKey')))
    
    with open(self.dir + '/' + self.config.get('Config','ExpensesFile'), 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([expense[1], float(expense[0].strip()) * -1, datetime.datetime.now(), self.user])
    self.user = self.config.get('Config','Users').split(',')
    return ('Logged expense: ' + str(self.command) + "\n").decode("utf8")  + self.doCommand('budget')
    
def expenses_get(self):
    f = open(self.dir + '/' + self.config.get('Config','ExpensesFile'), 'r')
    self.sendDocument(self.user, f)
    return ''