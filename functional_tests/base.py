# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Docs at https://selenium-python.readthedocs.io/waits.html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# Docs at https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
from selenium.webdriver.support import expected_conditions as EC
# Docs at https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.select.html
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from django.test import LiveServerTestCase
from django.urls import resolve, reverse
from budgets.models import Category

class FunctionalTest(LiveServerTestCase):
  # chromium true 11.931s
  # chormium false 16.099s
  # firefox true 16.813s ~ 42.180s
  # firefox false 17.952s
  BROWSER = "Firefox"
  HEADLESS = True

  @classmethod
  def setUpClass(self):
    super(FunctionalTest, self).setUpClass()
    self.setup_browser(self.BROWSER,self.HEADLESS)

  @classmethod
  def setup_browser(self, browser="Firefox", headless= True):
    if browser == "Firefox":
      options = Options()
      if headless:
        options.add_argument('-headless')
      self.browser = webdriver.Firefox(options=options)
    else:
      options = webdriver.ChromeOptions()
      options.add_argument('--ignore-certificate-errors')
      options.add_argument("--test-type")
      options.add_argument('--no-proxy-server')
      if headless:
        options.add_argument('--headless')
        # You need this if running the tests as root (run as root!?)
        # options.add_argument('--no-sandbox')
      options.binary_location = "/usr/bin/chromium-browser"
      self.browser = webdriver.Chrome(chrome_options=options)


  @classmethod
  def tearDownClass(self):
    super(FunctionalTest, self).setUpClass()
    self.browser.quit()

  # Credits to Tommy Beadle: http://disq.us/p/x1r1v2
  def wait_for_page_to_reload(self):
    if self.BROWSER == "Firefox":
      MAX_DELAY = 3
      wait = WebDriverWait(self.browser, MAX_DELAY)
      old_page = self.browser.find_element_by_tag_name('html')
      element = wait.until(EC.staleness_of(old_page))
    else:
      # TODO investigate why chromium does work without this
      pass

  def find_text_inside_table(self,text, table):
    rows = table.find_elements_by_tag_name('td')
    self.assertTrue(
      any(text in row.text for row in rows),
      f"No {text} in rows. Contents were\n{table.text}",
    )

  def assert_text_is_not_inside_table(self,text, table):
    rows = table.find_elements_by_tag_name('td')
    self.assertFalse(
      any(text in row.text for row in rows),
      f"Text {text} has been found! Contents were\n{table.text}",
    )

  def create_a_category(self, category_name, verify_creation=True):
    # Users create a category
    url = reverse('categories')
    self.browser.get(f"{self.live_server_url}{url}")

    inputbox = self.browser.find_element_by_id('id_new_category')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a new category'
    )

    if category_name:
      inputbox.send_keys(category_name)
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_page_to_reload()

    if verify_creation:
      self.verify_category_was_created(category_name)

  def create_an_expense(self, amount, category_name, note, expense_date):
    # Users visit expenses url
    url = reverse('expenses')
    self.browser.get(f"{self.live_server_url}{url}")
    # They see an input box
    inputbox = self.browser.find_element_by_id('id_new_expense_amount')
    # They input the price of the expense item
    inputbox.send_keys(amount)
    # They see a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_expenses_category'))
    # TODO The dropdown includes the Category they've just created
    # They choose that category
    dropdown.select_by_visible_text(category_name)

    # They see an input box
    note_inputbox = self.browser.find_element_by_id('id_new_expense_note')
    # They enter a note abotu the expenses, so that later they remember what this was about
    note_inputbox.send_keys(note)

    # They see an input box
    date_inputbox = self.browser.find_element_by_id('id_new_expense_date')
    # They enter the date of when the expenses was made
    date_inputbox.send_keys(expense_date)

    # They see a submit button
    submit_button = self.browser.find_element_by_id('id_submit')
    # # They click the button to save the entry
    submit_button.click()

    # They can see the information the correct information on the page
    self.verify_expense_was_created(amount,category_name,note)

    # The page reload and the expense item thye've entered is displayed correctly
    # TODO code smell, this wait_for_page_to_reload() should be needed
    # self.wait_for_page_to_reload()

  def verify_category_was_created(self, category_name):
    # They see the category name is present on the page
    table = self.browser.find_element_by_id('id_categories')
    self.find_text_inside_table(category_name, table)

  def verify_expense_was_created(self, amount, category_name, note):
    # They see all the details about the expese displayed on the page
    table = self.browser.find_element_by_id('id_expenses')
    self.find_text_inside_table(str(amount), table)
    self.find_text_inside_table(category_name, table)
    self.find_text_inside_table(note, table)
    # TODO: the view will print the date using the browser locale, the following line will fail
    # self.find_text_inside_table('2019-08-04', table)

