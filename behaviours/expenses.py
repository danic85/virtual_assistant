#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import os
import calendar
import lib.currency
from behaviours.behaviour import Behaviour


class Expenses(Behaviour):

    routes = {
        '^([$-1234567890.]*) ([a-zA-Z\s]*)': 'log_expense',
        'budget|how much money': 'expenses_remaining_weekly'
        # 'get expenses': 'expenses_get' # @todo allow files to be sent in response
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'expenses'

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
        with open(self.current_file(), 'rt') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                remaining += float(row[1].strip())
        response = 'There is £' + str(format(remaining, '.2f')) + ' left this month.'
        return response

    def expenses_remaining_weekly(self):
        income = 0.0
        expenses = 0.0
        remaining = 0.0
        with open(self.current_file(), 'rt') as csvfile:
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
        return response

    def log_expense(self):
        # expense = self.act.command['text'].split(' ', 1)
        amount, description = self.match.groups()
        expense = [amount, description]
        print(expense)

        if expense[0].find("$") == 0:
            expense[0] = str(lib.currency.convert(self, 'USD', expense[0].replace('$', ''),
                                                  self.config.get('Config', 'OpenExchangeRatesKey')))

        expense[0] = float(expense[0].strip()) * -1
        expense.append('')
        expense.append(datetime.datetime.now())
        expense.append(None)
        return self.write_to_file(expense)

    def write_to_file(self, expense):
        with open(self.current_file(), 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print(expense)
            csvwriter.writerow([expense[1], expense[0], expense[3], self.act.user, expense[2]])
        self.act.user = self.config.get('Config', 'Users').split(',')
        self.act.chain_command('budget')
        return 'Logged expense: ' + str(expense[0] * -1) + " " + expense[1] + "\n"

    def transaction_exists(self, transaction_id):
        if os.path.isfile(self.current_file()):
            with open(self.current_file(), 'rt') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in csvreader:
                    if len(row) > 4 and row[4].strip() == transaction_id.strip():
                        return True
        return False

    def expenses_get(self):
        if os.path.isfile(self.current_file()):
            f = open(self.current_file(), 'r')
            self.sendDocument(self.user, f)

        if os.path.isfile(self.last_file()):
            f = open(self.last_file(), 'r')
            self.sendDocument(self.user, f)

        return ''
