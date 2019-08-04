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
class ExpensesTest(FunctionalTest):

  def test_can_create_expense(self):
    CATEGORY_NAME = 'Rent'

    # Users create a category
    self.browser.get(f"{self.live_server_url}/categories")
    inputbox = self.browser.find_element_by_id('id_new_category')

    inputbox.send_keys(CATEGORY_NAME)
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_page_to_reload()

    # Users visit expenses url
    url = reverse('expenses')
    self.browser.get(f"{self.live_server_url}{url}")
    # They see an input box
    inputbox = self.browser.find_element_by_id('id_new_expense_amount')
    # They input the price of the expense item
    inputbox.send_keys(500)
    # They see a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_expenses_category'))
    # TODO The dropdown includes the Category they've just created
    # They choose that category
    dropdown.select_by_visible_text(CATEGORY_NAME)

    # They press the ENTER button
    inputbox.send_keys(Keys.ENTER)
    # The page reload and the expense item thye've entered is displayed correctly
    self.wait_for_page_to_reload()
    table = self.browser.find_element_by_id('id_expenses')
    self.find_text_inside_table(CATEGORY_NAME, table)
    self.find_text_inside_table(str(500), table)
    # TODO: the view will print the date using the browser locale, the following line will fail
    # self.find_text_inside_table('2019-08-04', table)