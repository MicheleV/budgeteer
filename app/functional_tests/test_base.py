# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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
    """Base Functional test class"""
    BROWSER = "Firefox"
    HEADLESS = True

    # Setup
    @classmethod
    def setUpClass(self):  # pylint: disable=C0103,C0202; # noqa
        super().setUpClass()
        self.setup_browser(self.BROWSER, self.HEADLESS)

    @classmethod
    def setup_browser(self, browser="Firefox", headless=True):  # pylint: disable=C0202; # noqa
        """Initialize the browser

        This browser instance is re-used for all tests in order to improve
        functional tests speed, as this operation is very expensive"""
        if browser == "Firefox":
            options = Options()
            if headless:
                options.add_argument('-headless')
            self.browser = webdriver.Firefox(options=options)
        # fallback to chromium otherwise
        else:
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--test-type")
            options.add_argument('--no-proxy-server')
            if headless:
                options.add_argument('--headless')
                # Note: if running the tests as root (why would we!?) add:
                # options.add_argument('--no-sandbox')
            options.binary_location = "/usr/bin/chromium-browser"
            self.browser = webdriver.Chrome(chrome_options=options)

        test_target = os.environ.get('TEST_TARGET')
        if test_target:
            self.live_server_url = f"http://{test_target}"

    @classmethod
    def tearDownClass(self):  # pylint: disable=C0103,C0202; # noqa
        super().setUpClass()
        self.browser.quit()

    def _call_each_method_in_module(module, tester):
        for name in dir(module):
            if name.startswith('test'):
                test_function = getattr(module, name)
                if callable(test_function):
                    # TODO: this will print function decorated with @skip as
                    # well even if they are not actually called
                    print(f"Calling {module.__name__}.{name}")  # pylint: disable=E1101; # noqa
                    test_function(tester)

    def test_categories(tester):
        """Execute functional tests related to all Categories"""
        FunctionalTest._call_each_method_in_module(Categories, tester)

    def test_expenses(tester):
        """Execute functional tests related to Expenses"""
        FunctionalTest._call_each_method_in_module(Expenses, tester)

    def test_monthly_budgets(tester):
        """Execute functional tests related to monthly budgets"""
        FunctionalTest._call_each_method_in_module(MBudgets, tester)

    def test_monthly_balances(tester):
        """Execute functional tests related to monthly balances"""
        FunctionalTest._call_each_method_in_module(MonthlyBalances, tester)

    def test_access(tester):
        """Execute functional tests to ensure all the pages in the nav are
        accessibles"""
        FunctionalTest._call_each_method_in_module(PageAccess, tester)

    def test_views_and_layout(tester):
        """Execute functional tests to confirm style is applied correctly"""
        FunctionalTest._call_each_method_in_module(ViewAndLayout, tester)

    def test_api(tester):  # TODO: this should be moved to the api own module
        """Execute tests for the API app"""
        FunctionalTest._call_each_method_in_module(API, tester)
