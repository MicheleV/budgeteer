# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import resolve, reverse
from django.test import TestCase
import budgets.models as m


class BaseTest(TestCase):

    def check_if_title_is_displayed(self, url_name, title):
        response = self.get_response_from_named_url(url_name)
        self.assertContains(response, title)

    def check_if_correct_view(self, url_name, view_func):
        url = reverse(url_name)
        found = resolve(url)
        self.assertEqual(found.func, view_func)

    def create_category(self, text):
        category = m.Category()
        category.text = text
        category.full_clean()
        category.save()
        return category

    def create_expense(self, category, amount, note, date):
        expense = m.Expense()
        expense.category = category
        expense.amount = amount
        expense.note = note
        expense.date = date
        expense.full_clean()
        expense.save()
        return expense

    def create_monthly_budgets(self, category, amount, date):
        budget = m.MonthlyBudget()
        budget.category = category
        budget.amount = amount
        budget.date = date
        budget.full_clean()
        budget.save()
        return budget

    def get_response_from_named_url(self, named_url):
        url = reverse(named_url)
        response = self.client.get(url)
        return response

    def check_if_error_matches(self, text, rows):
        self.assertTrue(
            any(text in row for row in rows),
            f"No {text} in rows. Contents were\n{rows}",
        )

    def create_income_category(self, text):
        category = m.IncomeCategory()
        category.text = text
        category.full_clean()
        category.save()
        return category

    def create_income(self, category, amount, note, date):
        expense = m.Income()
        expense.category = category
        expense.amount = amount
        expense.note = note
        expense.date = date
        expense.full_clean()
        expense.save()
        return expense

    def create_monthly_balance_category(self, text):
        mbc = m.MonthlyBalanceCategory()
        mbc.text = text
        mbc.full_clean()
        mbc.save()
        return mbc

    def create_monthly_balance(self, category, amount, date):
        mb = m.MonthlyBalance()
        mb.category = category
        mb.amount = amount
        mb.date = date
        mb.full_clean()
        mb.save()
        return mb
