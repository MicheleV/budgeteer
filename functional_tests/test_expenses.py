# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse

# TODO add negative test
# I.e. try to post with missing fields, etc
def test_can_not_create_malformed_expenses(self):
  # TODO at the moment being, empty memo field will succeed
  pass

# TODO duplicate code, move to utilities
def helper(self, amount, category_name):
  # Frank sees all the details sum  displayed on the page
  table = self.browser.find_element_by_id('id_expenses_total')
  self.find_text_inside_table(str(amount), table)
  self.find_text_inside_table(category_name, table)

def test_expenses_sum_appears_on_home_page(self):
  category_name = 'Rent'
  first_amount = 500
  second_amount = 420
  total_amount = first_amount + second_amount
  self.create_a_category(category_name)

  # Frank visits the expenses url and enters the expense details
  self.create_an_expense(
    first_amount,
    category_name,
    'First month of rent',
    '2019-08-09'
  )

  # Frank visits the expenses url again and enters a second expense with its details
  self.create_an_expense(
    second_amount,
    category_name,
    'Second month of rent (discounted)',
    '2019-09-09'
  )

  # Frank sees the sum of this month expenses on the home page
  url = reverse('expenses')
  self.browser.get(f"{self.live_server_url}{url}")
  helper(self, total_amount, category_name)
