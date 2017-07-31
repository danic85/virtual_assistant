#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import Mock, call, patch, mock_open
import datetime
from lib.interaction import Interaction
from behaviours import expenses
import re, os
from freezegun import freeze_time
import json
from lib import feeds

class TestExpensesMethods(unittest.TestCase):

    def test_routes(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        act = Interaction()
        b.logging = Mock()
        b.logging.info = Mock(return_value=True)

        b.log_expense = Mock()
        b.expenses_remaining_weekly = Mock()
        b.expenses_remaining = Mock()
        b.expenses_get = Mock()

        response = b.handle(act)
        self.assertEqual(response, None)

        act.command = {'text': 'budget'}
        b.handle(act)
        b.expenses_remaining_weekly.assert_called_once()

        act.command = {'text': 'get expenses'}
        b.handle(act)
        b.expenses_get.assert_called_once()

        act.command = {'text': '12.35 test expense'}
        b.handle(act)
        b.log_expense.assert_called_once()
        self.assertEqual(b.match.group(1), '12.35')
        self.assertEqual(b.match.group(2), 'test expense')

    @freeze_time('2017-01-01')
    def test_log_expense(self):
        b = expenses.Expenses(db=None, config={'users': "1234,12345"}, dir='')
        b.config = Mock()
        b.config.get = Mock(return_value='1234,12345')
        b.act = Mock()
        b.act.user = Mock()

        b.match = re.search('^([$-1234567890.]*) ([a-zA-Z\s]*)', '12.35 test expense', re.IGNORECASE)
        b.write_to_file = Mock(return_value='There is £-12.35 left this month.')

        self.assertEqual(b.log_expense(), 'There is £-12.35 left this month.')
        b.write_to_file.assert_called_with([-12.35, 'test expense', '', datetime.datetime(2017, 1, 1, 0, 0), None])

    @freeze_time('2017-01-01')
    def test_log_expense_dollars(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/expenses_convert.json'
        with open(path) as data_file:
            data = json.load(data_file)

        feeds.get_json = Mock()
        feeds.get_json.side_effect = [data]

        b = expenses.Expenses(db=None, config={}, dir='')
        b.act = Mock()
        b.act.user = Mock()

        b.config = Mock()
        b.config.get = Mock(return_value='1234,12345')

        b.match = re.search('^([$-1234567890.]*) ([a-zA-Z\s]*)', '$12.35 test expense', re.IGNORECASE)
        b.write_to_file = Mock(return_value='There is £-12.35 left this month.')

        self.assertEqual(b.log_expense(), 'There is £-12.35 left this month.')
        b.write_to_file.assert_called_with([-9.69228, 'test expense', '', datetime.datetime(2017, 1, 1, 0, 0), None])

    @freeze_time('2017-01-01')
    def test_write_to_file(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        b.act = Interaction()
        b.act.user = [1]
        b.config = Mock()
        b.config.get = Mock(return_value='1234,12345')
        mocked_open = mock_open(read_data='file contents\nas needed\n')
        with patch('behaviours.expenses.open', mocked_open, create=True):
            response = b.write_to_file([-12.35, 'test expense', '', datetime.datetime(2017, 1, 1, 0, 0), None])
            self.assertEqual(response, 'Logged expense: 12.35 test expense\n')
            self.assertEqual(b.act.response, [])

    @freeze_time('2017-06-11')
    def test_expenses_remaining(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata'
        b.files = path
        self.assertEqual(b.expenses_remaining(), 'There is £254.52 left this month.')

    @freeze_time('2017-06-11')
    def test_expenses_remaining_weekly(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata'
        b.files = path
        self.assertEqual(b.expenses_remaining_weekly(), 'There is £-188.81 left this week and £254.52 left this month')

    @freeze_time('2017-06-30')
    def test_expenses_remaining_weekly_end_of_month(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata'
        b.files = path
        self.assertEqual(b.expenses_remaining_weekly(), 'There is £254.52 left this week and £254.52 left this month')

    @freeze_time('2017-06-11')
    def test_transaction_exists(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata'
        b.files = path
        self.assertEqual(b.transaction_exists('tx_00009L1nuw673zQExkYbxp'), True)

    @freeze_time('2017-06-11')
    def test_transaction_exists_fail(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata'
        b.files = path
        self.assertEqual(b.transaction_exists('tx_00009L1nuw673zQExkYbx'), False)

    @freeze_time('2017-06-11')
    def test_expenses_get(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        b.act = Interaction()
        b.act.user = [1]

        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata'
        b.files = path
        b.expenses_get()

        print(b.act.response)
        self.assertEqual(len(b.act.response), 2)

        pattern = '^.*/tests/testdata/expenses/expenses-2017-.\.csv$'
        for r in b.act.response:
            match = re.search(pattern, r['path'], re.IGNORECASE)
            assert match

    @freeze_time('2017-01-11')
    def test_expenses_get_jan(self):
        b = expenses.Expenses(db=None, config={}, dir='')
        b.act = Interaction()
        b.act.user = [1]

        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata'
        b.files = path
        b.expenses_get()

        print(b.act.response)
        self.assertEqual(len(b.act.response), 2)

        pattern = '^.*/tests/testdata/expenses/expenses-201.-.+\.csv$'
        for r in b.act.response:
            match = re.search(pattern, r['path'], re.IGNORECASE)
            assert match

