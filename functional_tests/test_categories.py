# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import functional_tests.helpers as Helpers


def test_cant_create_an_empty_category(self):
    category_text = None
    Helpers.create_a_category(self, category_text, False)

    # Verify we do not have any category (No category with ID 1)
    table = self.browser.find_element_by_id('id_categories')
    Helpers.assert_text_is_not_inside_table(self, '1', table)


def test_can_create_multiple_categories(self):
    # Frank can create a category to log expenses related to his rent
    Helpers.create_a_category(self, 'Rent')
    # Frank can create a category to log his food expenses
    Helpers.create_a_category(self, 'Food')
