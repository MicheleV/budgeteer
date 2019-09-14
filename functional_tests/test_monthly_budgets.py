# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
from django.urls import resolve, reverse
import functional_tests.helpers as Helpers


def test_cant_create_an_empty_monthly_budget(self):
    # TODO Franks wants to create a budget but being confused,
    pass


def test_can_create_multiple_monthly_budgets(self):
    # Frank creates a category to log expenses related his rent
    category_name = 'Rent'
    Helpers.create_a_category(self, category_name)

    # Frank notices the home page is complaining about missing budgets for the
    # current month
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    table = self.browser.find_element_by_id('id_expenses_total')
    missing_budget_err = "No monthly budget for this month"
    Helpers.find_text_inside_table(self, missing_budget_err, table)

    budget_date = datetime.date.today().replace(day=1)
    amount = 7000
    Helpers.create_a_monthly_budget(self, category_name, amount, budget_date)

    # Frank notices the home page shows that amount he has set, and the notice
    # has disappeared
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    table = self.browser.find_element_by_id('id_expenses_total')
    Helpers.find_text_inside_table(self, str(amount), table)
    Helpers.find_text_inside_table(self, category_name, table)

    # Frank hopes that one day he will not have to do this operation every
    # month, but the system will remember his preferences and automatically
    # do this *boring* operation for him
    # TODO when a new month starts, monthly budgets for that month
    # should be cloned from the previous one
    # self.fail("Write me!")


def test_cant_create_multiple_monthly_budgets_for_same_month(self):
    # TODO Franks wants to update the budget amount
    pass
