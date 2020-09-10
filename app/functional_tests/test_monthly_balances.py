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


def test_diff_users_can_create_monthly_balance_cat_with_the_same_name(tester):
    # Frank can create a category to log his expenses
    cat_name = Helpers.generateString()

    Helpers.create_user(tester)
    Helpers.create_a_category(tester, category_name=cat_name, is_balance=True)
    Helpers.logout_user(tester)

    # Guido can create a category with the same name
    Helpers.create_user(tester)
    Helpers.create_a_category(tester, category_name=cat_name,
                              midway_check=True, create_check=False,
                              lack_of_error=True, is_balance=True)
    Helpers.logout_user(tester)


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


def users_cant_see_other_users_balance_categories(tester):
    # Frank can create a category to log his balance
    cat_name = Helpers.generateString()

    username, password = Helpers.create_user(tester)
    Helpers.create_a_category(tester, category_name=cat_name, is_balance=True)
    Helpers.logout_user(tester)

    # Guido can not see Frank's income category
    username_2, password_2 = Helpers.create_user(tester)

    Helpers.visit_and_verify_categories(tester, cat_name, is_income=False,
                                        should_exist=True, is_balance=True)

    Helpers.logout_user(tester)
