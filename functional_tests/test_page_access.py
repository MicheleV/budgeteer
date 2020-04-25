# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse


def test_can_access_page(self, named_url, title):
    url = reverse(named_url)
    self.browser.get(f"{self.live_server_url}{url}")
    self.assertIn(title, self.browser.title)


def test_cant_access_admin_page(self):
    self.browser.get(f"{self.live_server_url}/admin")
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('not found', header_text.lower())


def test_access_to_all_pages(self):
    test_can_access_page(self, 'home', 'Budgeteer')
    test_can_access_page(self, 'categories', 'Categories')
    test_can_access_page(self, 'expenses', 'Expense')
    test_can_access_page(self, 'monthly_budgets', 'Monthly budgets')
    test_can_access_page(self, 'income_categories', 'Income Categories')
    test_can_access_page(self, 'incomes', 'Incomes')
    test_can_access_page(self, 'goals', 'Goals')
    test_cant_access_admin_page(self)
