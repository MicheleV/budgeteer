# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse
import datetime
# TODO add negative test
# I.e. try to post with missing fields, etc
def test_can_not_create_malformed_expenses(self):
  # TODO at the moment being, empty memo field will succeed
  pass

# TODO duplicate code, move to utilities
def check_amount_and_cat_name(self, amount, category_name):
  # Frank sees all the details sum  displayed on the page
  table = self.browser.find_element_by_id('id_expenses_total')
  self.find_text_inside_table(str(amount), table)
  self.find_text_inside_table(category_name, table)

def create_category_and_two_expenses(self, first_amount, second_amount, category_name):
  self.create_a_category(category_name)

  # Frank visits the expenses url and enters the expense details
  self.create_an_expense(
    first_amount,
    category_name,
    'First month of rent',
    # TODO change this to be dynamic, otherwise tests will get flanky after Sep 2019
    '2019-08-09'
  )

  # Frank visits the expenses url again and enters a second expense with its details
  self.create_an_expense(
    second_amount,
    category_name,
    'Second month of rent (discounted)',
    # TODO change this to be dynamic, otherwise tests will get flanky after Sep 2019
    '2019-12-09',
    # Note False, since this expense is in the future (see comment above)
    False
  )

def check_whether_current_month_date_is_displayed(self):
  today_string = datetime.date.today().strftime("%Y-%m")
  date_container = self.browser.find_element_by_id('id_current_month_date')
  self.assertIn(today_string, date_container.text)

def without_paramters_expenses_page_shows_only_current_month_expenses(self, current_month_amount, category_name):
  table = self.browser.find_element_by_id('id_expenses_total')
  self.find_text_inside_table(str(current_month_amount), table)

def test_expenses_sum_appear_on_home_page(self):
  category_name = 'Rent'
  current_mont_amount = 500
  future_month_amount = 420
  total_amount = current_mont_amount + future_month_amount
  create_category_and_two_expenses(self, current_mont_amount, future_month_amount, category_name)

  # Frank sees the sum of this month expenses on the home page
  url = reverse('expenses')
  self.browser.get(f"{self.live_server_url}{url}")
  check_amount_and_cat_name(self, current_mont_amount, category_name)

  # Frank notices that the current month id displayed in the expense page
  check_whether_current_month_date_is_displayed(self)

  # Frank also notices that only expenses related to the current month are displayed
  without_paramters_expenses_page_shows_only_current_month_expenses(self, current_mont_amount, category_name)

def test_expenses_page_can_show_old_expenses(self):
  # TODO
  pass

def test_expenses_page_defaults_to_current_month_expenses_for_date_in_the_future(self):
  # TODO
  pass

def test_creating_expenses_without_first_creating_a_category_will_fail(self):
  # TODO
  pass