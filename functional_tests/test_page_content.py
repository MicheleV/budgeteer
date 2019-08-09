# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from django.urls import reverse
from .base import FunctionalTest

class PageContentTest(FunctionalTest):

  def test_home_page_has_link_categories_page(self):
    first_url_to_find = reverse('categories')
    second_url_to_find = reverse('expenses')

    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")

    links = self.browser.find_elements_by_tag_name('a')
    # TODO code smell, this should be refactored in a helper function when get a
    # third link
    self.assertTrue(
      any(first_url_to_find in link.get_attribute('href') for link in links),
      f"No url: {url} was found in the Page. links were\n{links}",
    )
    self.assertTrue(
      any(second_url_to_find in link.get_attribute('href') for link in links),
      f"No url: {url} was found in the Page. links were\n{links}",
    )

  # Verify css is properly loaded
  def test_layout_and_styling(self):
      # Credits http://www.obeythetestinggoat.com/book/chapter_prettification.html#_static_files_in_django
      # User loads the page
      url = reverse('categories')
      self.browser.get(f"{self.live_server_url}{url}")
      self.browser.set_window_size(1024, 768)

      # User notices the input box is nicely centered
      inputbox = self.browser.find_element_by_id('id_new_category')
      self.assertAlmostEqual(
          inputbox.location['x'] + inputbox.size['width'] / 2,
          512,
          delta=10
      )