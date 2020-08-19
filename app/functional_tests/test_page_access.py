# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse

import functional_tests.helpers as Helpers


def test_can_access_page(self, named_url, title):
    url = reverse(named_url)
    self.browser.get(f"{self.live_server_url}{url}")
    self.assertIn(title, self.browser.title)


def test_cant_access_admin_page(self):
    self.browser.get(f"{self.live_server_url}/admin")
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('not found', header_text.lower())


@Helpers.register_and_login
def test_access_to_all_pages(self):
    test_can_access_page(self, 'budgets:landing_page', 'Budgeteer')

    # Frank notices they are all browseable: Frank is happy
    test_can_access_page(self, 'budgets:home', 'Budgeteer')
    test_can_access_page(self, 'budgets:categories', 'Categories')
    test_can_access_page(self, 'budgets:expenses', 'Expense')
    test_can_access_page(self, 'budgets:monthly_budgets', 'Monthly budgets')
    test_can_access_page(self, 'budgets:income_categories', 'Income Categories')
    test_can_access_page(self, 'budgets:incomes', 'Incomes')
    test_can_access_page(self, 'budgets:goals', 'Goals')
    test_cant_access_admin_page(self)
