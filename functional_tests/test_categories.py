# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import resolve, reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from budgets.models import Category
from unittest import skip
from .base import FunctionalTest

class CategoriesTest(FunctionalTest):

  def test_can_create_categories(self):
    url = reverse('categories')
    self.browser.get(f"{self.live_server_url}{url}")
    inputbox = self.browser.find_element_by_id('id_new_category')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a new category'
    )

    inputbox.send_keys('Rent')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_page_to_reload()

    table = self.browser.find_element_by_id('id_categories')
    self.find_text_inside_table('Rent', table)

    inputbox = self.browser.find_element_by_id('id_new_category')

    inputbox.send_keys('Food')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_page_to_reload()

    table = self.browser.find_element_by_id('id_categories')
    self.find_text_inside_table('Food', table)

    # @skip
    def test_cannot_add_empty_categories(self):
      url = reverse('categories')
      self.browser.get(f"{self.live_server_url}{url}")

      self.browser.find_element_by_id('id_new_category').send_keys(Keys.ENTER)
      self.wait_for_page_to_reload()

      self.assertEqual(
        self.browser.find_element_by_css_selector('.has_error').text,
        "You can't have empty Categories"
      )

      self.fail("TODO: finish me")
