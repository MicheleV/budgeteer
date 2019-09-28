# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse
from datetime import date, timedelta
import functional_tests.helpers as Helpers


# TODO add negative test
# I.e. try to post with missing fields, etc
def test_cant_create_malformed_expenses(self):
    # TODO use Helpers.wait_for_required_input(self, "id_text")
    pass


# TODO add test in which Franks does not select any Categoy from the dropdown
def test_cant_create_expenses_without_selecting_a_category(self):
    # TODO use Helpers.wait_for_required_input(self, "id_text")
    pass


def test_expenses_sum_appear_on_home_page(self):
    category_name = 'Rent'
    curr_mont_amount = 500
    next_month_amount = 420
    first_expense = [
      curr_mont_amount,
      'First month of rent'
    ]
    second_expense = [
      next_month_amount,
      'Second month of rent (discounted)'
    ]
    total_amount = curr_mont_amount + next_month_amount

    Helpers.create_category_and_two_expenses(self, first_expense,
                                             second_expense, category_name)

    # Frank sees the sum of this month expenses on the home page
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    Helpers.check_amount_and_cat_name(self, curr_mont_amount, category_name)

    # Frank notices that the current month id displayed in the expense page
    Helpers.check_whether_current_month_date_is_displayed(self)

    # Frank also notices that only expenses related to the current month are
    # displayed
    Helpers.check_current_month(self, curr_mont_amount, category_name)


def test_expenses_page_can_show_old_expenses(self):
    # TODO: implement a get parameter and a dropdown to jump there
    pass


def test_expenses_wont_show_expenses_in_the_future(self):
    # TODO
    pass


def test_creating_expenses_before_categories_will_fail(self):
    # TODO
    pass
