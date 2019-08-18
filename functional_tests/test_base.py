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
import functional_tests.test_categories as TestCategories
import functional_tests.test_expenses as TestExpenses
import functional_tests.test_monthly_budgets as TestMonthlyBudgets
import functional_tests.test_page_access as TestPageAccess
import functional_tests.test_views_and_layout as TestViewsAndLayout

# Docs at https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TransactionTestCase
# Credits to 4c5 https://stackoverflow.com/users/267540/e4c5
# https://stackoverflow.com/questions/36988906/
# Given that TransactionTestCase is very slow,
# I've merged all the Instances of LiveServerTestCase so that we avoid the overhead
class FunctionalTest(LiveServerTestCase):
  BROWSER = "Firefox"
  HEADLESS = True

  ## Setup
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

  ## Helpers
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

  def find_url_in_home_page(self, url_to_find):
    url = reverse('home')
    self.browser.get(f"{self.live_server_url}{url}")

    links = self.browser.find_elements_by_tag_name('a')

    self.assertTrue(
      any(url_to_find in link.get_attribute('href') for link in links),
      f"No url: {url_to_find} was found in the Page. links were\n{links}",
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

  def create_a_monthly_budget(self, category_name, amount, date, verify_creation=True):
    # Frank visits the monthly expenses page
    url = reverse('monthly_budgets')
    self.browser.get(f"{self.live_server_url}{url}")

    # Frank sees an input box
    inputbox = self.browser.find_element_by_id('id_new_monthly_expenses_amount')
    # Frank inputs the price of the expense item
    inputbox.send_keys(amount)
    # Frank sees a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_budget_category'))
    # The dropdown includes the Category they want to set a budget for
    # Frank chooses that category
    dropdown.select_by_visible_text(category_name)

    # Frank sees another input box
    date_inputbox = self.browser.find_element_by_id('id_new_budget_date')
    # Frank enters the date for the budget
    date_inputbox.send_keys(date)

    # Frank finds the submit button
    submit_button = self.browser.find_element_by_id('id_submit')
    # Frank clicks the button to save the entry
    submit_button.click()

    if verify_creation:
      self.verify_monthly_expense_was_created(category_name, amount, date)

  def create_an_expense(self, amount, category_name, note, expense_date, verify_creation=True):
    # Users visit expenses page
    url = reverse('expenses')
    self.browser.get(f"{self.live_server_url}{url}")
    # They see an input box
    inputbox = self.browser.find_element_by_id('id_new_expense_amount')
    # They input the price of the expense item
    inputbox.send_keys(amount)
    # They see a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_expenses_category'))
    # The dropdown includes the Category they've just created
    # They choose that category
    dropdown.select_by_visible_text(category_name)

    # They see another input box
    note_inputbox = self.browser.find_element_by_id('id_new_expense_note')
    # They enter a note abotu the expenses, so that later they remember what this was about
    note_inputbox.send_keys(note)

    # They see one more input box
    date_inputbox = self.browser.find_element_by_id('id_new_expense_date')
    # They enter the date of when the expenses was made
    date_inputbox.send_keys(expense_date)

    # They see a submit button
    submit_button = self.browser.find_element_by_id('id_submit')
    # They click the button to save the entry
    submit_button.click()

    if verify_creation:
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

  def verify_monthly_expense_was_created(self, category_name, amount, date):
    # Frank sees all the details about the monghtly budget displayed on the page
    table = self.browser.find_element_by_id('id_monthly_budgets')
    self.find_text_inside_table(str(amount), table)
    self.find_text_inside_table(category_name, table)
    # TODO: the view will print the date using the browser locale, the following line will fail
    # self.find_text_inside_table('2019-08-04', table)

  ## Actual tests
  def test_categories_first_set(self):
    TestCategories.test_cannot_create_an_empty_category(self)
    TestCategories.test_can_create_multiple_categories(self)

  def test_expenses(self):
    TestExpenses.test_can_create_multiple_expense(self)
    TestExpenses.test_can_not_create_malformed_expenses(self)

  def test_monthly_budgets(self):
    TestMonthlyBudgets.test_cannot_create_an_empty_monthly_budget(self)
    TestMonthlyBudgets.test_can_create_multiple_monthly_budgets(self)
    TestMonthlyBudgets.test_can_not_create_multiple_monthly_budgets_for_the_same_month(self)

  def test_access(self):
    TestPageAccess.test_can_access_home_page(self)
    TestPageAccess.test_can_access_list_categories_page(self)
    TestPageAccess.test_can_access_list_expenses_page(self)
    TestPageAccess.test_cannot_access_admin_page(self)

  def test_views_and_layout(self):
    TestViewsAndLayout.test_home_page_has_link_categories_page(self)
    TestViewsAndLayout.test_layout_and_styling(self)