# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
from unittest import skip

from django.urls import resolve
from django.urls import reverse

import functional_tests.helpers as Helpers


def test_cant_create_an_empty_monthly_budget(self):
    # TODO Franks wants to create a budget but being confused,
    # he enters an empty sum and tries to press 'Submit'...
    # ...Nothing happens!
    pass


@skip
@Helpers.register_and_login
def test_can_create_multiple_monthly_budgets(self):
    # Frank creates a category to log expenses related his rent
    category_name = 'Rent'
    Helpers.create_a_category(self, category_name)

    # Frank notices the home page is NOT complaining about missing budgets for
    # the current month <- TODO: fix me
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    table = self.browser.find_element_by_id('id_expenses_total')
    # TODO: change this as we now hide categories without a monthly budget
    # missing_budget_err = "No monthly budget for this month"
    # Helpers.find_text_inside_table(self, missing_budget_err, table)

    budget_date = datetime.date.today().replace(day=1)
    amount = 7000
    Helpers.create_a_monthly_budget(self, category_name, amount, budget_date)

    # Frank notices the home page shows that amount he has set
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    table = self.browser.find_element_by_id('id_expenses_total')
    Helpers.find_text_inside_table(self, str(amount), table)
    Helpers.find_text_inside_table(self, category_name, table)

    # Frank logs a fraction of his rent (he was confused with this previous
    # apartment)
    wrong_amt = 4000
    note = 'First month of rent'
    rent_date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
    is_income = False
    Helpers.create_entry(self, wrong_amt, category_name, note,
                         rent_date, is_income)

    # Frank notices that the home page is showing he still has room for
    # spending, in the Rent category
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    remainder = amount - wrong_amt
    table = self.browser.find_element_by_id('id_expenses_total')
    formatted_amount = f'{remainder:n}'
    Helpers.find_text_inside_table(self, str(formatted_amount), table)

    # Frank also notices the amount is green, meaning he still has room for
    # spending!
    # TODO, check for "text-danger" class

    # Frank notices his error and logs the full amount of the rent
    # creating a new expenses (Frank can't find how to edit an entry)
    remainder = 5000
    note = 'First month of rent'
    rent_date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
    is_income = False
    Helpers.create_entry(self, remainder, category_name, note,
                         rent_date, is_income)

    # Frank now notices he is overspending, he should have not moved!
    # TODO, check for "text-success" class

    # Frank hopes that one day he will not have to do this operation every
    # month, but the system will remember his preferences and automatically
    # do this *boring* operation for him
    # TODO when a new month starts, monthly budgets for that month
    # should be cloned from the previous one
    # self.fail("Write me!")


@skip
@Helpers.register_and_login
def test_cant_create_multiple_monthly_budgets_for_same_month(self):

    # Frank creates a category to log expenses related his rent
    category_name = 'Rent'
    Helpers.create_a_category(self, category_name)

    # Frank knows he also has to create a budget for the current month
    # so he proceed to create one
    budget_date = datetime.date.today().replace(day=1)
    amount = 7000
    Helpers.create_a_monthly_budget(self, category_name, amount, budget_date)

    # Frank however has been up till very late the day before, and is quite
    # distracted. Accidentally he repeats the same procedure again
    Helpers.create_a_monthly_budget(self, category_name, amount, budget_date)

    # However an error promtply notifies him that this is not allowed
    error = 'Monthly budget with this Category and Date already exists.'
    Helpers.find_error(self, error)


# TODO: add a test to verify the monthly budgets are displayed
# in date desc order

# TODO: add tests for mass creation
