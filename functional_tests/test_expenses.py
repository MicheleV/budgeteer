# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse
from datetime import date, timedelta
import functional_tests.helpers as Helpers


def create_category_and_two_expenses(self, first_amount, second_amount,
                                     category_name):
    Helpers.create_a_category(self, category_name)

    first_date = date.today().replace(day=1)
    delta = timedelta(weeks=10)
    second_date = first_date + delta

    # Frank visits the expenses url and enters the expense details
    Helpers.create_an_expense(
      self,
      first_amount,
      category_name,
      'First month of rent',
      first_date.strftime("%Y-%m-%d")
    )

    # Frank visits the expenses url again and enters a second expense with its
    # details
    Helpers.create_an_expense(
      self,
      second_amount,
      category_name,
      'Second month of rent (discounted)',
      second_date.strftime("%Y-%m-%d"),
      # Note False, since this expense is in the future (see comment above)
      False
    )


def check_whether_current_month_date_is_displayed(self):
    today_string = date.today().strftime("%Y-%m")
    date_container = self.browser.find_element_by_id('id_current_month_date')
    self.assertIn(today_string, date_container.text)


def exp_shows_only_current_month(self, current_month_amount, category_name):
    """
    Expenses page will show only expenses from the current month when acccessed
    without paramters
    """
    table = self.browser.find_element_by_id('id_expenses_total')
    Helpers.find_text_inside_table(self, str(current_month_amount), table)


# TODO add negative test
# I.e. try to post with missing fields, etc
def test_cant_create_malformed_expenses(self):
    # TODO at the moment being, empty memo field will succeed
    pass


def test_expenses_sum_appear_on_home_page(self):
    category_name = 'Rent'
    current_mont_amount = 500
    future_month_amount = 420
    total_amount = current_mont_amount + future_month_amount
    create_category_and_two_expenses(self, current_mont_amount,
                                     future_month_amount, category_name)

    # Frank sees the sum of this month expenses on the home page
    url = reverse('expenses')
    self.browser.get(f"{self.live_server_url}{url}")
    Helpers.check_amount_and_cat_name(self, current_mont_amount, category_name)

    # Frank notices that the current month id displayed in the expense page
    check_whether_current_month_date_is_displayed(self)

    # Frank also notices that only expenses related to the current month are
    # displayed
    exp_shows_only_current_month(self, current_mont_amount, category_name)


def test_expenses_page_can_show_old_expenses(self):
    # TODO: implement a get parameter and a dropdown to jump there
    pass


def test_expenses_wont_show_expenses_in_the_future(self):
    # TODO
    pass


def test_creating_expenses_before_categories_will_fail(self):
    # TODO
    pass
