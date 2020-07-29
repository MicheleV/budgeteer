# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os

from django.test import LiveServerTestCase
from django.urls import resolve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from budgets.models import Category
import functional_tests.helpers as Helpers
import functional_tests.test_api as API
import functional_tests.test_categories as Categories
import functional_tests.test_expenses as Expenses
import functional_tests.test_monthly_balances as MonthlyBalances
import functional_tests.test_monthly_budgets as MBudgets
import functional_tests.test_page_access as PageAccess
import functional_tests.test_views_and_layout as ViewAndLayout

# Docs at https://docs.djangoproject.com/en/2.2/topics/testing/
# tools/#django.test.TransactionTestCase
# Credits to 4c5 https://stackoverflow.com/users/267540/e4c5
# https://stackoverflow.com/questions/36988906/
# Given that TransactionTestCase is very slow,
# I've merged all the Instances of LiveServerTestCase so that
# we avoid the overhead


class FunctionalTest(LiveServerTestCase):
    BROWSER = "Firefox"
    HEADLESS = True

    # Setup
    @classmethod
    def setUpClass(self):
        super(FunctionalTest, self).setUpClass()
        self.setup_browser(self.BROWSER, self.HEADLESS)

    @classmethod
    def setup_browser(self, browser="Firefox", headless=True):
        if browser == "Firefox":
            options = Options()
            if headless:
                options.add_argument('-headless')
            self.browser = webdriver.Firefox(options=options)
        # Uses chromium if not Firefox
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

        test_target = os.environ.get('TEST_TARGET')
        if test_target:
            self.live_server_url = f"http://{test_target}"

    @classmethod
    def tearDownClass(self):
        super(FunctionalTest, self).setUpClass()
        self.browser.quit()

    # Actual tests
    def test_categories(self):
        Categories.test_cant_create_an_empty_expense_category(self)
        Categories.test_can_create_multiple_expense_categories(self)
        Categories.test_cant_create_duplicate_expense_categories(self)

    def test_expenses(self):
        Expenses.test_cant_create_malformed_expenses(self)
        Expenses.test_expenses_sum_appear_on_home_page(self)
        Expenses.test_expenses_page_can_show_old_expenses(self)
        Expenses.test_expenses_wont_show_expenses_in_the_future(self)
        Expenses.test_creating_expenses_before_categories_will_fail(self)
        Expenses.test_cant_create_expenses_without_selecting_a_category(self)
        Expenses.test_only_expenses_in_range_are_shown(self)

    def test_monthly_budgets(self):
        MBudgets.test_cant_create_an_empty_monthly_budget(self)
        MBudgets.test_can_create_multiple_monthly_budgets(self)
        MBudgets.test_cant_create_multiple_monthly_budgets_for_same_month(self)

    def test_monthly_balances(self):
        MonthlyBalances.test_image_is_not_displayed_without_data(self)
        MonthlyBalances.test_image_is_displayed_with_data(self)

    def test_access(self):
        PageAccess.test_access_to_all_pages(self)

    def test_views_and_layout(self):
        ViewAndLayout.test_home_page_has_links_in_nav(self)
        ViewAndLayout.test_layout_and_styling(self)
        ViewAndLayout.check_autofocus(self)

    def test_api(self):
        API.test_create_and_delete_expenses(self)
