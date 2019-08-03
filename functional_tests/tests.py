# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

class FunctionalTest(LiveServerTestCase):

  @classmethod
  def setUpClass(self):
    super(FunctionalTest, self).setUpClass()
    self.browser = webdriver.Firefox()

  @classmethod
  def tearDownClass(self):
    super(FunctionalTest, self).setUpClass()
    self.browser.quit()

class PagesAccessTest(FunctionalTest):

  def test_can_access_home_page(self):
    self.browser.get(self.live_server_url)
    self.assertIn('Budgeteer', self.browser.title)

  def test_can_access_list_categories_page(self):
    self.browser.get(f"{self.live_server_url}/categories")
    header_text = self.browser.find_element_by_tag_name('title').text
    self.assertIn('Categories', self.browser.title)

  def test_cannot_access_admin_page(self):
    self.browser.get(f"{self.live_server_url}/admin")
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('Not Found', header_text)

class CreateCategoriesTest(FunctionalTest):

  def test_can_create_category(self):
    self.browser.get(f"{self.live_server_url}/categories")
    inputbox = self.browser.find_element_by_id('id_new_category')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a new category'
    )

    inputbox.send_keys('Rent')
    inputbox.send_keys(Keys.ENTER)
    time.sleep(3)

    table = self.browser.find_element_by_id('id_categories')
    rows = table.find_elements_by_tag_name('td')

    self.assertTrue(
      any('Rent' in row.text for row in rows),
      f"No Rent in rows. Contents were\n{table.text}",
    )

    self.fail('Finish the test!')