# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Docs at https://selenium-python.readthedocs.io/waits.html
from datetime import date
from datetime import timedelta
import locale
import string
import random
# Docs at https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/
#  selenium.webdriver.support.expected_conditions.html
from django.urls import resolve, reverse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


locale.setlocale(locale.LC_ALL, '')
MAX_DELAY = 3


# TODO: duplicate code from unit tests
def generateString(length=10):
    """
    Generate a random string of a given length
    """
    char = string.ascii_lowercase
    return ''.join(random.choice(char) for i in range(length))


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
        # TODO: investigate why chromium does work without this
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
    url = reverse('budgets:home')
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


def register_and_login(func):
    """
    Decorator that create a random user, log in as it, and log out at the end
    """
    def wrapper(*args, **kwargs):
        create_user(*args, **kwargs)
        func(*args, **kwargs)
        logout_user(*args, **kwargs)
    return wrapper


def create_user(self, username=None, password=None):
    """
    Sign up, and automatically log in as said user
    """
    if not username:
        username = generateString()
    if not password:
        password = generateString()

    url = reverse('accounts:signup')
    self.browser.get(f"{self.live_server_url}{url}")

    # Frank sign up: first he enters a gibberish username, he likes privacy
    user_input_box = self.browser.find_element_by_id('id_username')
    user_input_box.send_keys(username)

    # Frank then insert a random password... Frank likes security
    pwd_input_1 = self.browser.find_element_by_id('id_password1')
    pwd_input_1.send_keys(password)

    # Frank re-inputs the same password, Frank really knows how web form works!
    pwd_input_2 = self.browser.find_element_by_id('id_password2')
    pwd_input_2.send_keys(password)

    # Frank see a submit button
    submit_button = self.browser.find_elements_by_tag_name('button')
    submit_button[0].click()

    return (username, password)


def logout_user(self):
    """
    Simply log out
    """
    url = reverse('accounts:logout')
    self.browser.get(f"{self.live_server_url}{url}")


# TODO: is_income is making the logic complex, refactor
def create_a_category(self, category_name,
                      is_income=False, create_check=True, midway_check=False):
    url = reverse('budgets:categories_create')
    if is_income:
        url = reverse('budgets:income_categories_create')

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

    # Check for error right after submitting the form
    if midway_check:
        find_error(self, 'Category with this Text already exists')

    # Check if the categoy page is showing created category
    if create_check:
        visit_and_verify_categories(self, category_name)


def create_a_monthly_budget(self, category_name, amount, date,
                            create_check=True):
    # Frank visits the monthly expenses page
    url = reverse('budgets:monthly_budgets_create')
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
        verify_monthly_expense_was_created(self, category_name,
                                           formatted_amount, date)


# TODO: is_income is making the logic complex, refactor
def create_entry(self, amount, category_name, note, expense_date,
                 is_income=False, verify_creation=True):
    # Frank visits the expenses page
    url = reverse('budgets:expenses_create')
    if is_income:
        url = reverse('budgets:incomes_create')

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


def visit_and_verify_categories(self, category_name, should_exist=True):
    url = reverse('budgets:categories')
    self.browser.get(f"{self.live_server_url}{url}")
    table = self.browser.find_element_by_id('id_categories')
    if should_exist:
        find_text_inside_table(self, category_name, table)
    else:
        # HACK: we check for ID 1, instead of category name
        assert_text_is_not_inside_table(self, '1', table)


# NOTE: deprecated
def verify_category_was_created(self, category_name):
    # Frank sees the category name is present on the page
    table = self.browser.find_element_by_id('id_categories')
    find_text_inside_table(self, category_name, table)


# NOTE: to be deprecated
def verify_expense_was_created(self, amount, category_name, note):
    # Frank sees all the details about the expense displayed on the page
    table = self.browser.find_element_by_id('id_expenses')
    find_text_inside_table(self, str(amount), table)
    find_text_inside_table(self, category_name, table)
    find_text_inside_table(self, note, table)
    # TODO: check for date! This is not browser dependent
    # find_text_inside_table('2019-08-04', table)


# NOTE: to be deprecated
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
