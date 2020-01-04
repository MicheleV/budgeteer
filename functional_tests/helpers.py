# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Docs at https://selenium-python.readthedocs.io/waits.html
from datetime import date
from datetime import timedelta
import locale

# Docs at https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/
#  selenium.webdriver.support.expected_conditions.html
from django.urls import resolve, reverse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

locale.setlocale(locale.LC_ALL, '')
MAX_DELAY = 3


def check_amount_and_cat_name(self, amount, category_name):
    # Frank sees all the details sum  displayed on the page
    table = self.browser.find_element_by_id('id_expenses_total')
    find_text_inside_table(self, str(amount), table)
    find_text_inside_table(self, category_name, table)


# Credits to Tommy Beadle: http://disq.us/p/x1r1v2
def wait_for_page_to_reload(self):
    if self.BROWSER == "Firefox":
        wait = WebDriverWait(self.browser, MAX_DELAY)
        old_page = self.browser.find_element_by_tag_name('html')
        element = wait.until(EC.staleness_of(old_page))
    else:
        # TODO investigate why chromium does work without this
        pass


def wait_for_required_input(self, elem_id):
    wait = WebDriverWait(self.browser, MAX_DELAY)
    invalid = self.browser.find_elements_by_css_selector(f"#{elem_id}:invalid")
    self.assertEqual(len(invalid), 1)


# TODO merge the two functions below
def find_text_inside_table(self, text, table):
    rows = table.find_elements_by_tag_name('td')
    self.assertTrue(
        any(text in row.text for row in rows),
        f"No {text} in rows. Contents were\n{table.text}",
    )


def assert_text_is_not_inside_table(self, text, table):
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


def find_error(self, errorText, printErrors=False):
    error_container = self.browser.find_element_by_class_name('errorlist')
    errors = error_container.find_elements_by_tag_name('li')

    if printErrors:
        for error in errors:
            print(error.text)

    self.assertTrue(
        any(errorText in error.text for error in errors),
        f"{errorText} was not present. Contents were\n{errors}",
    )


def create_a_category(self, category_name,
                      is_income=False, verify_creation=True):
    url = reverse('categories')

    if is_income:
        url = reverse('income_categories')
        is_income = True

    # Frank creates a category
    self.browser.get(f"{self.live_server_url}{url}")

    inputbox = self.browser.find_element_by_id('id_text')
    self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Enter a new category'
    )

    if category_name:
        inputbox.send_keys(category_name)
        inputbox.send_keys(Keys.ENTER)
        wait_for_page_to_reload(self)

    if verify_creation:
        verify_category_was_created(self, category_name)


def create_a_monthly_budget(self, category_name, amount, date,
                            verify_creation=True):
    # Frank visits the monthly expenses page
    url = reverse('monthly_budgets')
    self.browser.get(f"{self.live_server_url}{url}")

    # Frank sees an input box
    inputbox = self.browser.find_element_by_id('id_amount')
    # Frank inputs the price of the expense item
    inputbox.send_keys(amount)
    # Frank sees a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_category'))
    # The dropdown includes the Category Frank wants to set a budget for
    # Frank chooses that category
    dropdown.select_by_visible_text(category_name)

    # Frank sees another input box
    date_inputbox = self.browser.find_element_by_id('id_date')
    # Frank enters the date for the budget
    date_inputbox.send_keys(date.strftime("%Y-%m-%d"))

    # Frank finds the submit button
    submit_button = self.browser.find_element_by_id('id_submit')
    # Frank clicks the button to save the entry
    submit_button.click()

    if verify_creation:
        formatted_amount = f'{amount:n}'
        verify_monthly_expense_was_created(self, category_name, formatted_amount, date)


def create_entry(self, amount, category_name, note, expense_date,
                 is_income=False, verify_creation=True):
    # Frank visits the expenses page
    url = reverse('expenses')
    if is_income:
        url = reverse('incomes')

    self.browser.get(f"{self.live_server_url}{url}")
    # Frank sees an input box
    inputbox = self.browser.find_element_by_id('id_amount')
    # Frank inputs the price of the expense item
    inputbox.send_keys(amount)
    # Frank sees a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_category'))
    # The dropdown includes the Category they've just created
    # Frank chooses that category
    dropdown.select_by_visible_text(category_name)

    # Frank sees another input box
    note_inputbox = self.browser.find_element_by_id('id_note')
    # Frank enters a note abotu the expenses, so that later they remember what
    # this was about
    note_inputbox.send_keys(note)

    # Frank sees one more input box
    date_inputbox = self.browser.find_element_by_id('id_date')
    # Frank enters the date of when the expense was made
    date_inputbox.send_keys(expense_date)

    # Frank see a submit button
    submit_button = self.browser.find_element_by_id('id_submit')
    # Frank clicks the button to save the entry
    submit_button.click()

    if verify_creation:
        formatted_amount = f'{amount:n}'
        # Frank can see the information the correct information on the page
        verify_expense_was_created(self, formatted_amount, category_name, note)

    # The page reload and the expense entered item is displayed correctly
    # TODO code smell, this wait_for_page_to_reload() should be needed
    # wait_for_page_to_reload(self)


def create_category_and_two_expenses(self, first_item, second_item,
                                     category_name, is_income=False):
    create_a_category(self, category_name, is_income)

    first_date = date.today().replace(day=1)
    delta = timedelta(weeks=10)
    second_date = first_date - delta
    if is_income:
        method = create_entry
    else:
        method = create_entry
    # Frank visits the expenses url and enters the expense details
    method(
      self,
      first_item[0],
      category_name,
      first_item[1],
      first_date.strftime("%Y-%m-%d"),
      is_income
    )

    # Frank visits the expenses url again and enters a second expense with its
    # details
    method(
      self,
      second_item[0],
      category_name,
      second_item[1],
      second_date.strftime("%Y-%m-%d"),
      is_income,
      # Note False, since this expense is in the past, it should not appear
      False
    )


def verify_category_was_created(self, category_name):
    # Frank sees the category name is present on the page
    table = self.browser.find_element_by_id('id_categories')
    find_text_inside_table(self, category_name, table)


def verify_expense_was_created(self, amount, category_name, note):
    # Frank sees all the details about the expense displayed on the page
    table = self.browser.find_element_by_id('id_expenses')
    find_text_inside_table(self, str(amount), table)
    find_text_inside_table(self, category_name, table)
    find_text_inside_table(self, note, table)
    # TODO: check for date! This is not browser dependent
    # find_text_inside_table('2019-08-04', table)


def verify_monthly_expense_was_created(self, category_name, amount, date):
    # Frank sees all the details about the monghtly budget displayed on the
    # page
    table = self.browser.find_element_by_id('id_monthly_budgets')
    find_text_inside_table(self, str(amount), table)
    find_text_inside_table(self, category_name, table)
    year_month = date.strftime("%Y-%m")
    find_text_inside_table(self, year_month, table)

    # Franks visits the home page and sees the budget


def check_whether_current_month_date_is_displayed(self):
    """
    Current page should display the current date in '%Y-%m' format
    """
    today_string = date.today().strftime("%Y-%m")
    date_container = self.browser.find_element_by_id('id_current_month_date')
    self.assertIn(today_string, date_container.text)


def check_current_month(self, current_month_amount, category_name):
    """
    Current page should show only expenses from the current month when
    acccessed without paramters.
    """
    table = self.browser.find_element_by_id('id_expenses_total')
    find_text_inside_table(self, str(current_month_amount), table)
    # TODO add two expense in different months (current, past) and confirm
    # only the expense for the current month is displayed
