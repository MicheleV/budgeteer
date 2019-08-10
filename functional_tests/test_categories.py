# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import resolve, reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from budgets.models import Category
from unittest import skip
from .base import FunctionalTest

class CategoriesTest(FunctionalTest):

  def test_can_create_multiple_categories(self):
    # Users can create a category to log expenses related to their rent
    self.create_a_category('Rent')
    # Users can create a category to log their food expenses
    self.create_a_category('Food')

  def test_cannot_create_an_empty_category(self):
    category_text = None
    self.create_a_category(category_text, False)

    # Verify we do not have any category (No category with ID 1)
    table = self.browser.find_element_by_id('id_categories')
    self.assert_text_is_not_inside_table('1', table)
