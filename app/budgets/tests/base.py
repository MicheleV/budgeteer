# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from datetime import datetime
from functools import wraps
import os
import random
import string

from dotenv import load_dotenv

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve
from django.urls import reverse

import budgets.models as m

# Load env file ONCE: inside BaseTest class
load_dotenv()


class BaseTest(TestCase):

    def setUp(self):
        """
        BaseTest signup, called once per test (method)
        """
        self._sign_up()

    @staticmethod
    def generateString(length=10):
        """
        Generate a random string of a given length
        """
        char = string.ascii_lowercase
        return ''.join(random.choice(char) for i in range(length))

    def check_if_title_is_displayed(self, url_name, title):
        """
        Check whether the page has a title or not
        """
        response = self.get_response_from_named_url(url_name)
        self.assertContains(response, title)

    def check_if_correct_view(self, url_name, view_func):
        """
        Check whether a given view is using the correct function or not
        """
        url = reverse(url_name)
        found = resolve(url)
        self.assertEqual(found.func, view_func)

    def get_response_from_named_url(self, named_url, args=None):
        """
        Wrapper for get/post methods for a given named url
        """
        if args:
            url = reverse(named_url, kwargs=args)
            response = self.client.post(url)
        else:
            url = reverse(named_url)
            response = self.client.get(url)
        return response

    def check_if_error_matches(self, text, rows):
        """
        Compare the error text
        """
        self.assertTrue(
            any(text in row for row in rows),
            f"No {text} in rows. Contents were\n{rows}",
        )

    def _sign_up(self):
        """
        Create an user, and add a reference to self.user
        self.credentials is a dictionaru containing both username and password
        """
        text = self.generateString(50)
        pwd = self.generateString(10)
        username = self.generateString(10) + str(datetime.now())
        self.user = User.objects.create_user(
            username=username, password=pwd)
        self.credentials = {'username': username, 'password': pwd}
        self.password = pwd

    def _login(self):
        """
        Login an user
        """
        url = reverse('accounts:login')
        response = self.client.post(url, self.credentials, follow=True)

    def login(func):
        """
        Login decorator
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self._login()
            func(self, *args, **kwargs)

        return wrapper

    def signup_and_login(self):
        """Create an user, and log in using said user credentials"""
        self._sign_up()
        self._login()

    def _logout(self):
        """
        Logout an user
        """
        url = reverse('accounts:logout')
        response = self.client.get(url)

    def create_category(self, text):
        """
        Create a category
        """
        category = m.Category()
        category.text = text
        category.created_by = self.user
        category.full_clean()
        category.save()
        return category

    def create_expense(self, category, amount, note, date):
        """
        Create an expense
        """
        expense = m.Expense()
        expense.category = category
        expense.amount = amount
        expense.note = note
        expense.date = date
        expense.created_by = self.user
        expense.full_clean()
        expense.save()
        return expense

    def create_monthly_budgets(self, category, amount, date):
        """
        Create a monthly budget
        """
        budget = m.MonthlyBudget()
        budget.category = category
        budget.amount = amount
        budget.date = date
        budget.created_by = self.user
        budget.full_clean()
        budget.save()
        return budget

    def create_income_category(self, text):
        """
        Create an income category
        """
        category = m.IncomeCategory()
        category.text = text
        category.created_by = self.user
        category.full_clean()
        category.save()
        return category

    def create_income(self, category, amount, note, date):
        """
        Create an income
        """
        income = m.Income()
        income.category = category
        income.amount = amount
        income.note = note
        income.date = date
        income.created_by = self.user
        income.full_clean()
        income.save()
        return income

    def create_monthly_balance_category(self, text):
        """
        Create a monthly balance category
        """
        mbc = m.MonthlyBalanceCategory()
        mbc.text = text
        mbc.created_by = self.user
        mbc.full_clean()
        mbc.save()
        return mbc

    def create_monthly_balance(self, category, amount, date):
        """
        Create a monthly balance
        """
        mb = m.MonthlyBalance()
        mb.category = category
        mb.amount = amount
        mb.date = date
        mb.created_by = self.user
        mb.full_clean()
        mb.save()
        return mb

    def create_goal(self, amount, text, note, is_archived=False):
        """
        Create a goal
        """
        g = m.Goal()
        g.amount = amount
        g.text = text
        g.note = note
        g.is_archived = is_archived
        g.created_by = self.user
        g.full_clean()
        g.save()
        return g
