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
