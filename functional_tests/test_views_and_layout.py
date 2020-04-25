# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import reverse

import functional_tests.helpers as Helpers


def test_home_page_has_links_in_nav(self):
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")

    urls = [
     reverse('home'),
     reverse('categories'),
     reverse('expenses'),
     reverse('monthly_budgets'),
     reverse('income_categories'),
     reverse('incomes'),
     reverse('monthly_balance_categories'),
     reverse('monthly_balances'),
     reverse('goals'),
    ]

    for url in urls:
        Helpers.find_url_in_home_page(self, url)


# Credits http://www.obeythetestinggoat.com/book/
#         chapter_prettification.html#_static_files_in_django
# Verify css is properly loaded
def test_layout_and_styling(self):
    # Frank loads the page
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")
    self.browser.set_window_size(1024, 768)

    # Frank notices the logo at the bottom is nicely centered
    inputbox = self.browser.find_element_by_css_selector('#footer_text')
    self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
    )


def check_autofocus(self):

    urls = [
     reverse('categories'),
     reverse('income_categories'),
     reverse('monthly_balance_categories'),
    ]

    for url in urls:
        self.browser.get(f"{self.live_server_url}{url}")
        inputbox = self.browser.find_element_by_id('id_text')
        self.assertTrue(inputbox.get_attribute("autofocus"))
