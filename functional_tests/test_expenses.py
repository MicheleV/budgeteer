# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Docs at https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.select.html
from selenium.webdriver.support.ui import Select
from budgets.models import Category
from django.urls import reverse
from unittest import skip
from .base import FunctionalTest
import time
class ExpensesTest(FunctionalTest):

  def create_a_category(self, category_name):
    # Users create a category
    self.browser.get(f"{self.live_server_url}/categories")
    inputbox = self.browser.find_element_by_id('id_new_category')

    inputbox.send_keys(category_name)
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_page_to_reload()

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
    table = self.browser.find_element_by_id('id_expenses')
    self.find_text_inside_table(category_name, table)

  def verify_expense_was_created(self, amount, category_name, note):
    # They see all the details about the expese displayed on the page
    table = self.browser.find_element_by_id('id_expenses')
    self.find_text_inside_table(str(amount), table)
    self.find_text_inside_table(category_name, table)
    self.find_text_inside_table(note, table)
    # TODO: the view will print the date using the browser locale, the following line will fail
    # self.find_text_inside_table('2019-08-04', table)

  def test_can_create_multiple_expense(self):
    CATEGORY_NAME = 'Rent'
    self.create_a_category(CATEGORY_NAME)

    # Users visit expenses url and enters the expens details
    self.create_an_expense(
      500,
      CATEGORY_NAME,
      'First month of rent',
      '2019-08-09'
    )

    # Users visit expenses url again and enters a second expense with its details
    self.create_an_expense(
      420,
      CATEGORY_NAME,
      'Second month of rent (discounted)',
      '2019-09-09'
    )

  @skip
  def test_user_can_not_create_empty_categories(self):
    pass
  # TODO add negative test
  # I.e. try to post with missing fields, etc