# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from django.test import LiveServerTestCase
from django.urls import resolve
from budgets.models import Category
import functional_tests.helpers as Helpers
import functional_tests.test_categories as TestCategories
import functional_tests.test_expenses as TestExpenses
import functional_tests.test_monthly_budgets as TestMonthlyBudgets
import functional_tests.test_page_access as TestPageAccess
import functional_tests.test_views_and_layout as TestViewsAndLayout

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
        self.setup_browser(self.BROWSER,self.HEADLESS)

    @classmethod
    def setup_browser(self, browser="Firefox", headless= True):
        if browser == "Firefox":
            options = Options()
            if headless:
                options.add_argument('-headless')
            self.browser = webdriver.Firefox(options=options)
        # self.browser.set_window_size(1024, 768)
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

    # Actual tests
    def test_categories_first_set(self):
        TestCategories.test_cannot_create_an_empty_category(self)
        TestCategories.test_can_create_multiple_categories(self)

    def test_expenses(self):
        TestExpenses.test_can_not_create_malformed_expenses(self)
        TestExpenses.test_expenses_sum_appear_on_home_page(self)

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
