# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse
from django.urls import resolve

import functional_tests.helpers as Helpers

# FIX ME: this test will succeed for ANY failure, not only for missing images
@Helpers.register_and_login
def test_image_is_not_displayed_without_data(tester):

    # Frank has heard of this new graph feature
    # He opens the monthly balances page
    url = reverse('budgets:monthly_balances')
    tester.browser.get(f"{tester.live_server_url}{url}")
    images = tester.browser.find_elements_by_tag_name('img')
    # ...but he does not see any shiny graph!
    tester.assertEqual(len(images), 0)


def test_image_is_displayed_with_data(tester):
    # Frank enters some data (he wants to get his hands on the new graphs asap)
    # Frank finally opens the monthly balances page and see a shiny graph
    pass


# TODO:write me
def test_all_data_table_is_ordered_date_desc(tester):
    pass


# TODO:write me
def test_specific_month_data_shows_no_graph(tester):
    pass


# TODO:write me
def test_specific_month_data_shows_total(tester):
    pass


# TODO:write me
def test_check_whether_image_contains_correct_currency(tester):
    pass


# TODO:write me
def test_check_both_graph_and_right_side_table_are_shown(tester):
    pass

# TODO: add tests for mass creation