# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from unittest import skip

from django.urls import reverse

import functional_tests.helpers as Helpers


# FIX ME: this test will succeed for ANY failure, not only for creation failure
@Helpers.register_and_login
def test_cant_create_an_empty_expense_category(tester):
    text = ''

    Helpers.create_a_category(tester, category_name=text,
                              is_income=False, create_check=False,
                              wait_for_reload=False)

    # Frank notices his browser his forcing him to input something
    Helpers.wait_for_required_input(tester, "id_text")

    # Frank does not follows the browser instruction, and stares at the screen
    # in disdain. He thought he could create an empty expense Category
    Helpers.visit_and_verify_categories(tester, category_name=text,
                                        should_exist=False)


@Helpers.register_and_login
def test_can_create_multiple_expense_categories(tester):
    # Frank can create a category to log expenses related to his rent
    cat_name1 = Helpers.generateString()
    Helpers.create_a_category(tester, cat_name1)
    # Frank can create a category to log his food expenses
    cat_name2 = Helpers.generateString()
    Helpers.create_a_category(tester, cat_name2)


# @Helpers.register_and_login
def test_different_users_can_create_categories_with_the_same_name(tester):
    # Frank can create a category to log his expenses
    cat_name = Helpers.generateString()

    Helpers.create_user(tester)
    Helpers.create_a_category(tester, category_name=cat_name)
    Helpers.logout_user(tester)

    # Guido can create a category with the same name
    Helpers.create_user(tester)
    Helpers.create_a_category(tester, category_name=cat_name,
                              midway_check=True, create_check=False,
                              lack_of_error=True)
    Helpers.logout_user(tester)

# FIX ME: this test will succeed for ANY failure, not only for creation failure
@Helpers.register_and_login
def test_cant_create_duplicate_expense_categories(tester):
    # Frank can create a category to log expenses related to his rent
    text = Helpers.generateString()
    Helpers.create_a_category(tester, category_name=text, is_income=True)

    # Frank is not paying attention to what he is doing, and he tries
    # to create the same category
    Helpers.create_a_category(tester, category_name=text, is_income=True,
                              create_check=False, midway_check=True)


@Helpers.register_and_login
def test_cant_create_an_empty_income_category(tester):
    text = ''
    # with tester.assertRaises(TimeoutException) as e:
    Helpers.create_a_category(tester, category_name=text,
                              is_income=True,
                              create_check=False,
                              wait_for_reload=False)

    # Frank notices his browser his forcing him to input something
    Helpers.wait_for_required_input(tester, "id_text")

    url = reverse('budgets:categories')
    tester.browser.get(f"{tester.live_server_url}{url}")
    # Frank does not follows the browser instruction, and stares at the screen
    # in disdain. He thought he could create an empty income Category

    table = tester.browser.find_element_by_id('id_categories')
    Helpers.assert_text_is_not_inside_table(tester, text, table)


@Helpers.register_and_login
def test_can_create_multiple_income_categories(tester):
    # Frank can create a category to log his wages
    Helpers.create_a_category(tester, 'Wage',
                              is_income=True, create_check=True)
    # Frank can create a category to log the money he gets from his money tree
    Helpers.create_a_category(tester, 'MoneyTree',
                              is_income=True, create_check=True)


@Helpers.register_and_login
def test_cant_create_duplicate_income_categories(tester):
    # Frank can create a category to log expenses related to his rent
    Helpers.create_a_category(tester, 'Rent', is_income=True)

    # Frank is not paying attention to what he is doing, and he tries
    # to create the same category
    Helpers.create_a_category(tester, 'Rent', is_income=True,
                              midway_check=True)
