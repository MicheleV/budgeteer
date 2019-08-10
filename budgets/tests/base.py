# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse
from django.test import TestCase
from budgets.models import Category, Expense

class BaseTest(TestCase):

  def create_category(self, text):
    category = Category()
    category.text = text
    category.save()
    category.full_clean()
    return category

  def create_expense(self, category, amount, note, spended_date):
    first_expense = Expense()
    first_expense.category = category
    first_expense.amount = amount
    first_expense.note = note
    first_expense.spended_date = spended_date
    first_expense.save()
    first_expense.full_clean()
    return first_expense

  def get_response_from_named_url(self, named_url):
    url = reverse(named_url)
    response = self.client.get(url)
    return response
