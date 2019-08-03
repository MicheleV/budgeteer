# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from django.urls import reverse
from .base import FunctionalTest

class PageContentTest(FunctionalTest):

  def test_home_page_has_link_categories_page(self):
    url_to_find = reverse('categories')
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")

    links = self.browser.find_elements_by_tag_name('a')
    self.assertTrue(
      any(url_to_find in link.get_attribute('href') for link in links),
      f"No url: {url} was found in the Page. links were\n{links}",
    )
