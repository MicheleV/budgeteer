# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse


def test_can_access_home_page(self):
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    self.assertIn('Budgeteer', self.browser.title)


def test_can_access_list_categories_page(self):
    url = reverse('categories')
    self.browser.get(f"{self.live_server_url}{url}")
    self.assertIn('Categories', self.browser.title)


def test_can_access_list_expenses_page(self):
    url = reverse('expenses')
    self.browser.get(f"{self.live_server_url}{url}")
    self.assertIn('Expense', self.browser.title)


def test_cant_access_admin_page(self):
    self.browser.get(f"{  self.live_server_url}/admin")
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('not found', header_text.lower())
