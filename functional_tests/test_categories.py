# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import functional_tests.helpers as Helpers


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
    table = self.browser.find_element_by_id('id_categories')
    Helpers.assert_text_is_not_inside_table(self, '1', table)


def test_can_create_multiple_expense_categories(self):
    # Frank can create a category to log expenses related to his rent
    Helpers.create_a_category(self, 'Rent')
    # Frank can create a category to log his food expenses
    Helpers.create_a_category(self, 'Food')


def test_cant_create_duplicate_expense_categories(self):
    # Frank can create a category to log expenses related to his rent
    Helpers.create_a_category(self, 'Rent')

    # Frank is not paying attention to what he is doing, and he tries
    # to create the same category
    Helpers.create_a_category(self, 'Rent')
    Helpers.find_error(self, 'Category with this Text already exists')


def test_cant_create_an_empty_income_category(self):
    category_text = None
    is_income_category = True
    run_verification = False
    Helpers.create_a_category(self, category_text,
                              is_income_category, run_verification)

    # Frank notices his browser his forcing him to input something
    Helpers.wait_for_required_input(self, "id_text")

    # Frank does not follows the browser instruction, and stares at the screen
    # in disdain. He thought he could create an empty income Category
    table = self.browser.find_element_by_id('id_categories')
    Helpers.assert_text_is_not_inside_table(self, '1', table)


def test_can_create_multiple_income_categories(self):
    is_income_category = True
    run_verification = True
    # Frank can create a category to log his wages
    Helpers.create_a_category(self, 'Wage',
                              is_income_category, run_verification)
    # Frank can create a category to log the money he gets from his money tree
    Helpers.create_a_category(self, 'MoneyTree',
                              is_income_category, run_verification)


def test_cant_create_duplicate_income_categories(self):
    is_income_category = True

    # Frank can create a category to log expenses related to his rent
    Helpers.create_a_category(self, 'Rent', is_income_category)

    # Frank is not paying attention to what he is doing, and he tries
    # to create the same category
    Helpers.create_a_category(self, 'Rent', is_income_category)
    Helpers.find_erroor(self, 'Category with this Text already exists')
