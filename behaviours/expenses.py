#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import os
import calendar
from behaviours.behaviour import Behaviour
from lib import feeds


class Expenses(Behaviour):

    routes = {
        '^([$-1234567890.]*) ([a-zA-Z\s]*)': 'log_expense',
        'budget|how much money': 'expenses_remaining_weekly',
        'get expenses': 'expenses_get'
    }

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.collection = 'expenses'

    def expenses_remaining(self):
        remaining = 0.0
        with open(self.__current_file(), 'rt') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                remaining += float(row[1].strip())
        response = 'There is £' + str(format(remaining, '.2f')) + ' left this month.'
        return response

    def expenses_remaining_weekly(self):
        income = 0.0
        expenses = 0.0
        remaining = 0.0
        with open(self.__current_file(), 'rt') as csvfile:
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
            expense[0] = str(self.__convert('USD', expense[0].replace('$', ''),
                                                  self.config.get('OpenExchangeRatesKey')))

        expense[0] = float(expense[0].strip()) * -1
        expense.append('')
        expense.append(datetime.datetime.now())
        expense.append(None)
        return self.write_to_file(expense)

    def transaction_exists(self, transaction_id):
        """ Check that transaction exists (used for bank api integrations) """
        if os.path.isfile(self.__current_file()):
            with open(self.__current_file(), 'rt') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in csvreader:
                    if len(row) > 4 and row[4].strip() == transaction_id.strip():
                        return True
        return False

    def expenses_get(self):
        if os.path.isfile(self.__current_file()):
            self.act.respond_file(self.__current_file())

        if os.path.isfile(self.__last_file()):
            self.act.respond_file(self.__last_file())

        return ''

    def write_to_file(self, expense):
        with open(self.__current_file(), 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print(expense)
            csvwriter.writerow([expense[1], expense[0], expense[3], self.act.user, expense[2]])
        self.act.user = self.config.get('Users').split(',')
        self.act.chain_command('budget')
        return 'Logged expense: ' + str(expense[0] * -1) + " " + expense[1] + "\n"

    @staticmethod
    def __convert(currency, amount, key):
        """ Convert currency into GBP (as long as it's USD!) """
        endpoint = 'https://openexchangerates.org/api/latest.json?app_id=' + key

        r = feeds.get_json(endpoint, None)
        gbp = r['rates']['GBP']
        conversion = float(amount) * float(gbp)
        return conversion

    def __last_file(self):
        now = datetime.datetime.now()
        month = now.month - 1
        year = now.year
        if month < 1:
            month = 12
            year -= 1
        return self.files + '/expenses/expenses-' + str(year) + '-' + str(month) + '.csv'

    def __current_file(self):
        now = datetime.datetime.now()
        return self.files + '/expenses/expenses-' + str(now.year) + '-' + str(now.month) + '.csv'
