# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse

import functional_tests.helpers as Helpers


def _can_access_page(tester, named_url, title):
    url = reverse(named_url)
    tester.browser.get(f"{tester.live_server_url}{url}")
    tester.assertIn(title, tester.browser.title)


def _cant_access_admin_page(tester):
    tester.browser.get(f"{tester.live_server_url}/admin")
    header_text = tester.browser.find_element_by_tag_name('h1').text
    tester.assertIn('not found', header_text.lower())


@Helpers.register_and_login
def test_access_to_all_pages(tester):
    _can_access_page(tester, 'budgets:landing_page', 'Budgeteer')

    # Frank notices they are all browseable: Frank is happy
    _can_access_page(tester, 'budgets:home', 'Budgeteer')
    _can_access_page(tester, 'budgets:categories', 'Categories')
    _can_access_page(tester, 'budgets:expenses', 'Expense')
    _can_access_page(tester, 'budgets:monthly_budgets', 'Monthly budgets')
    _can_access_page(tester, 'budgets:income_categories', 'Income Categories')
    _can_access_page(tester, 'budgets:incomes', 'Incomes')
    _can_access_page(tester, 'budgets:goals', 'Goals')
    _cant_access_admin_page(tester)
