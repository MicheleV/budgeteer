# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from unittest import skip

from django.urls import reverse

import functional_tests.helpers as Helpers


# FIX ME: this test will succeed for ANY failure, not only for creation failure
# TODO: replace self with tester for readability, once we remove @skip
@Helpers.register_and_login
@skip
def test_cant_create_an_empty_expense_category(self):
    category_text = None
    is_income_category = False
    run_verification = False

    Helpers.create_a_category(self, category_text,
                              is_income_category, run_verification)

    # Frank notices his browser his forcing him to input something
    Helpers.wait_for_required_input(self, "id_text")

    # Frank does not follows the browser instruction, and stares at the screen
    # in disdain. He thought he could create an empty expense Category
    should_cat_exist = False
    Helpers.visit_and_verify_categories(self, category_text, should_cat_exist)
    # print(self.browser.find_element_by_tag_name('html').text)
    # table = self.browser.find_element_by_id('id_categories')
    # Helpers.assert_text_is_not_inside_table(self, '1', table)


@Helpers.register_and_login
def test_can_create_multiple_expense_categories(tester):
    # Frank can create a category to log expenses related to his rent
    cat_name1 = Helpers.generateString()
    Helpers.create_a_category(tester, cat_name1)
    # Frank can create a category to log his food expenses
    cat_name2 = Helpers.generateString()
    Helpers.create_a_category(tester, cat_name2)


# FIX ME: this test will succeed for ANY failure, not only for creation failure
@Helpers.register_and_login
@skip
def test_cant_create_duplicate_expense_categories(tester):
    # Frank can create a category to log expenses related to his rent
    Helpers.create_a_category(tester, 'Rent')

    # Frank is not paying attention to what he is doing, and he tries
    # to create the same category
    Helpers.create_a_category(tester, 'Rent', is_income=True,
                              create_check=False, midway_check=True)


@Helpers.register_and_login
def test_cant_create_an_empty_income_category(tester):
    category_text = ''
    is_income_category = True
    run_verification = False
    wait_for_reload = False

    # with tester.assertRaises(TimeoutException) as e:
    Helpers.create_a_category(tester, category_name=category_text,
                              is_income=is_income_category,
                              create_check=run_verification,
                              wait_for_reload=wait_for_reload)

    # Frank notices his browser his forcing him to input something
    Helpers.wait_for_required_input(tester, "id_text")

    url = reverse('budgets:categories')
    tester.browser.get(f"{tester.live_server_url}{url}")
    # Frank does not follows the browser instruction, and stares at the screen
    # in disdain. He thought he could create an empty income Category

    table = tester.browser.find_element_by_id('id_categories')
    Helpers.assert_text_is_not_inside_table(tester, category_text, table)


@Helpers.register_and_login
def test_can_create_multiple_income_categories(tester):
    is_income_category = True
    run_verification = True
    # Frank can create a category to log his wages
    Helpers.create_a_category(tester, 'Wage',
                              is_income_category, run_verification)
    # Frank can create a category to log the money he gets from his money tree
    Helpers.create_a_category(tester, 'MoneyTree',
                              is_income_category, run_verification)


@Helpers.register_and_login
def test_cant_create_duplicate_income_categories(tester):
    is_income_category = True

    # Frank can create a category to log expenses related to his rent
    Helpers.create_a_category(tester, 'Rent', is_income_category)

    # Frank is not paying attention to what he is doing, and he tries
    # to create the same category
    midway_check = True
    Helpers.create_a_category(tester, 'Rent', is_income_category, midway_check=midway_check)
