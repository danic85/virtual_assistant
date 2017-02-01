#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import os
import calendar
import lib.currency


def last_file(self):
    now = datetime.datetime.now()
    month = now.month - 1
    year = now.year
    if month < 1:
        month = 12
        year -= 1
    return self.files + '/expenses/expenses-' + str(year) + '-' + str(month) + '.csv'


def current_file(self):
    now = datetime.datetime.now()
    return self.files + '/expenses/expenses-' + str(now.year) + '-' + str(now.month) + '.csv'


def expenses_remaining(self):
    remaining = 0.0
    with open(current_file(self), 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            remaining += float(row[1].strip())
    response = 'There is £' + str(format(remaining, '.2f')) + ' left this month.'
    return response.decode("utf8")


def expenses_remaining_weekly(self):
    income = 0.0
    expenses = 0.0
    remaining = 0.0
    with open(current_file(self), 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            val = float(row[1].strip())
            if val > 0:
                income += val
            else:
                expenses += val
            remaining += val

    now = datetime.datetime.now()
    today = datetime.date.today()

    # get the number of days to next monday
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    days_to_next_monday = next_monday.day - 1  # ignore monday
    # Set to end of month if next monday is in next month
    if next_monday.month > now.month:
        days_to_next_monday = days_in_month

    # Calculate daily budget and remaining budget for the current week
    daily_budget = income / days_in_month
    budget_to_date = daily_budget * days_to_next_monday
    remaining_week = budget_to_date - abs(expenses)

    response = 'There is £' + str(format(remaining_week, '.2f'))
    response += ' left this week and £' + str(format(remaining, '.2f')) + ' left this month'
    return response.decode("utf8")


def expenses_add(self):
    expense = self.command.split(' ', 1)
    if expense[0].find("$") == 0:
        expense[0] = str(lib.currency.convert(self, 'USD', expense[0].replace('$', ''),
                                              self.config.get('Config', 'OpenExchangeRatesKey')))

    with open(current_file(self), 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([expense[1], float(expense[0].strip()) * -1, datetime.datetime.now(), self.user])
    self.user = self.config.get('Config', 'Users').split(',')
    return ('Logged expense: ' + str(self.command) + "\n").decode("utf8") + self.do_command('budget')


def expenses_get(self):
    if os.path.isfile(current_file(self)):
        f = open(current_file(self), 'r')
        self.sendDocument(self.user, f)

    if os.path.isfile(last_file(self)):
        f = open(last_file(self), 'r')
        self.sendDocument(self.user, f)

    return ''
