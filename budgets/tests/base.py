# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse
from django.test import TestCase
from budgets.models import Category, Expense, MonthlyBudget

class BaseTest(TestCase):

  def create_category(self, text):
    category = Category()
    category.text = text
    category.save()
    category.full_clean()
    return category

  def create_expense(self, category, amount, note, spended_date):
    expense = Expense()
    expense.category = category
    expense.amount = amount
    expense.note = note
    expense.spended_date = spended_date
    expense.save()
    expense.full_clean()
    return expense

  def create_monthly_budgets(self, category, amount, date):
    budget = MonthlyBudget()
    budget.category = category
    budget.amount = amount
    budget.date = date
    budget.save()
    budget.full_clean()
    return budget

  def get_response_from_named_url(self, named_url):
    url = reverse(named_url)
    response = self.client.get(url)
    return response
