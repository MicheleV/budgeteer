# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import functional_tests.helpers as Helpers
from django.urls import reverse, resolve


def test_image_is_not_displayed_without_data(self):
    # Frank has heard of this new graph feature
    # He opens the monthly balances page
    url = reverse('monthly_balances')
    self.browser.get(f"{self.live_server_url}{url}")
    images = self.browser.find_elements_by_tag_name('img')
    # ...but he does not see any shiny graph!
    self.assertEqual(len(images), 0)


def test_image_is_displayed_with_data(self):
    # Frank enters some data (he wants to get his hands on the new graphs asap)
    # Frank finally opens the monthly balances page and see a shiny graph
    pass
