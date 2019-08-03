# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Docs at https://selenium-python.readthedocs.io/waits.html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# Docs at https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from django.urls import reverse
from budgets.models import Category

class FunctionalTest(LiveServerTestCase):

  @classmethod
  def setUpClass(self):
    super(FunctionalTest, self).setUpClass()
    self.browser = webdriver.Firefox()

  @classmethod
  def tearDownClass(self):
    super(FunctionalTest, self).setUpClass()
    self.browser.quit()

  # Credits to Tommy Beadle: http://disq.us/p/x1r1v2
  def wait_for_page_to_reload(self):
    MAX_DELAY = 5
    wait = WebDriverWait(self.browser, MAX_DELAY)
    old_page = self.browser.find_element_by_tag_name('html')
    element = wait.until(EC.staleness_of(old_page))

  def find_text_inside_table(self,text, table):
    rows = table.find_elements_by_tag_name('td')
    self.assertTrue(
      any(text in row.text for row in rows),
      f"No {text} in rows. Contents were\n{table.text}",
    )

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

class CategoriesTest(FunctionalTest):

  def test_can_create_category(self):
    self.browser.get(f"{self.live_server_url}/categories")
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