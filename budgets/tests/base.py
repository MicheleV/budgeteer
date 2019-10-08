# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse
from django.test import TestCase
import budgets.models as m


class BaseTest(TestCase):

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
