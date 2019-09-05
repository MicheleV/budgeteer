# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Docs at https://selenium-python.readthedocs.io/waits.html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# Docs at https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/
#  selenium.webdriver.support.expected_conditions.html
from selenium.webdriver.support import expected_conditions as EC
from django.urls import resolve, reverse


def check_amount_and_cat_name(self, amount, category_name):
    # Frank sees all the details sum  displayed on the page
    table = self.browser.find_element_by_id('id_expenses_total')
    find_text_inside_table(self, str(amount), table)
    find_text_inside_table(self, category_name, table)


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


def create_a_category(self, category_name, verify_creation=True):
    # Frank creates a category
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
        wait_for_page_to_reload(self)

    if verify_creation:
        verify_category_was_created(self, category_name)


def create_a_monthly_budget(self, category_name, amount, date,
                            verify_creation=True):
    # Frank visits the monthly expenses page
    url = reverse('monthly_budgets')
    self.browser.get(f"{self.live_server_url}{url}")

    # Frank sees an input box
    inputbox = self.browser.find_element_by_id('id_new_monthly_expenses_amount')
    # Frank inputs the price of the expense item
    inputbox.send_keys(amount)
    # Frank sees a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_budget_category'))
    # The dropdown includes the Category Frank wants to set a budget for
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
        verify_monthly_expense_was_created(self, category_name, amount, date)


def create_an_expense(self, amount, category_name, note, expense_date,
                      verify_creation=True):
    # Frank visits the expenses page
    url = reverse('expenses')
    self.browser.get(f"{self.live_server_url}{url}")
    # Frank sees an input box
    inputbox = self.browser.find_element_by_id('id_new_expense_amount')
    # Frank inputs the price of the expense item
    inputbox.send_keys(amount)
    # Frank sees a dropdown
    dropdown = Select(self.browser.find_element_by_id('id_expenses_category'))
    # The dropdown includes the Category they've just created
    # Frank chooses that category
    dropdown.select_by_visible_text(category_name)

    # Frank sees another input box
    note_inputbox = self.browser.find_element_by_id('id_new_expense_note')
    # Frank enters a note abotu the expenses, so that later they remember what
    # this was about
    note_inputbox.send_keys(note)

    # Frank sees one more input box
    date_inputbox = self.browser.find_element_by_id('id_new_expense_date')
    # Frank enters the date of when the expense was made
    date_inputbox.send_keys(expense_date)

    # Frank see a submit button
    submit_button = self.browser.find_element_by_id('id_submit')
    # Frank clicks the button to save the entry
    submit_button.click()

    if verify_creation:
        # Frank can see the information the correct information on the page
        verify_expense_was_created(self, amount, category_name, note)

    # The page reload and the expense entered item is displayed correctly
    # TODO code smell, this wait_for_page_to_reload() should be needed
    # wait_for_page_to_reload(self)


def verify_category_was_created(self, category_name):
    # Frank sees the category name is present on the page
    table = self.browser.find_element_by_id('id_categories')
    find_text_inside_table(self, category_name, table)


# TODO duplicate code, move to utilities
def verify_expense_was_created(self, amount, category_name, note):
    # Frank sees all the details about the expense displayed on the page
    table = self.browser.find_element_by_id('id_expenses')
    find_text_inside_table(self, str(amount), table)
    find_text_inside_table(self, category_name, table)
    find_text_inside_table(self, note, table)
    # TODO: the view will print the date using the browser locale, the
    # following line will fail
    # find_text_inside_table('2019-08-04', table)


def verify_monthly_expense_was_created(self, category_name, amount, date):
    # Frank sees all the details about the monghtly budget displayed on the
    # page
    table = self.browser.find_element_by_id('id_monthly_budgets')
    find_text_inside_table(self, str(amount), table)
    find_text_inside_table(self, category_name, table)
    find_text_inside_table('2019-08', table)
