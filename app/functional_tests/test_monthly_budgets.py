# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
import random

import functional_tests.helpers as Helpers


def test_cant_create_an_empty_monthly_budget(tester):
    # TODO Franks wants to create a budget but being confused,
    # he enters an empty sum and tries to press 'Submit'...
    # ...Nothing happens!
    pass


@Helpers.register_and_login
def test_can_create_multiple_monthly_budgets(tester):
    # Frank creates a category to log expenses related his rent
    category_name = Helpers.generate_string()
    Helpers.create_a_category(tester, category_name)

    budget_date = datetime.date.today().replace(day=1)
    amount = 7000
    Helpers.create_a_monthly_budget(tester, category_name=category_name,
                                    amount=amount, date=budget_date)

    # Frank logs a fraction of his rent (he got confused with this previous
    # apartment)
    wrong_amt = 4000
    note = 'First month of rent'
    rent_date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
    is_income = False
    Helpers.create_entry(tester, amount=wrong_amt, category_name=category_name,
                         note=note, expense_date=rent_date, is_income=is_income)

    # FIX ME: we're not displaying the monthly bugets anymore!!!

    # Frank notices the home page shows that amount he has set
    # url = reverse('budgets:home')
    # tester.browser.get(f"{tester.live_server_url}{url}")

    # table = tester.browser.find_element_by_id('id_expenses_total')
    # Helpers.find_text_inside_table(tester, str(amount), table)
    # Helpers.find_text_inside_table(tester, category_name, table)

    # # Frank notices that the home page is showing he still has room for
    # # spending, in the Rent category
    # url = reverse('budgets:home')
    # tester.browser.get(f"{tester.live_server_url}{url}")
    # remainder = amount - wrong_amt
    # table = tester.browser.find_element_by_id('id_expenses_total')
    # formatted_amount = f'{remainder:n}'
    # Helpers.find_text_inside_table(tester, str(formatted_amount), table)

    # Frank also notices the amount is green, meaning he still has room for
    # spending!
    # TODO, check for "text-danger" class

    # Frank notices his error and logs the full amount of the rent
    # creating a new expenses (Frank can't find how to edit an entry)
    remainder = 5000
    note = Helpers.generate_string()
    rent_date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
    is_income = False
    Helpers.create_entry(tester, amount=remainder, category_name=category_name,
                         note=note, expense_date=rent_date,
                         is_income=is_income)

    # Frank now notices he is overspending, he should have not moved!
    # TODO, check for "text-success" class

    # Frank hopes that one day he will not have to do this operation every
    # month, but the system will remember his preferences and automatically
    # do this *boring* operation for him
    # TODO when a new month starts, monthly budgets for that month
    # should be cloned from the previous one
    # self.fail("Write me!")


@Helpers.register_and_login
def test_cant_create_multiple_monthly_budgets_for_same_month(tester):

    # Frank creates a category to log expenses related his rent
    category_name = Helpers.generate_string()
    Helpers.create_a_category(tester, category_name)

    # Frank knows he also has to create a budget for the current month
    # so he proceeds to create one
    budget_date = datetime.date.today().replace(day=1)
    amount = 7000
    Helpers.create_a_monthly_budget(tester, category_name=category_name,
                                    amount=amount, date=budget_date)

    # Frank however has been up till very late the day before, and is quite
    # distracted. Accidentally he repeats the same procedure again
    Helpers.create_a_monthly_budget(tester, category_name=category_name,
                                    amount=amount, date=budget_date,
                                    create_check=False)

    # However an error promtply notifies him that this is not allowed
    Helpers.wait_for_page_to_reload(tester)
    error = 'Monthly budget with this Category and Date already exists.'
    Helpers.find_error(tester, error)


# TODO:write me
def test_can_monhtly_balances_are_displayed_in_date_desc_order(tester):
    pass


# TODO:write me
def test_can_create_multiple_monhtly_balances_at_once(tester):
    pass
    # TODO: add tests for mass creation


def test_users_cant_see_other_users_monthly_budgets(tester):
    Helpers.create_user(tester)

    # Frank creates a category to log expenses related his rent
    category_name = Helpers.generate_string()
    Helpers.create_a_category(tester, category_name)

    # Frank knows he also has to create a budget for the current month
    # ...so he proceeds to create one
    budget_date = datetime.date.today().replace(day=1)
    amount = random.randint(1, 90000)
    Helpers.create_a_monthly_budget(tester, category_name=category_name,
                                    amount=amount, date=budget_date)
    Helpers.logout_user(tester)

    # Guido can not see Frank's monthly budget
    Helpers.create_user(tester)

    Helpers.visit_and_verify_month_budget_creation(tester=tester,
                                                   category_name=category_name,
                                                   amount=amount,
                                                   date=budget_date,
                                                   should_exist=False)
    Helpers.logout_user(tester)
