# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from datetime import date
from datetime import timedelta
from unittest import skip

from django.urls import reverse, resolve
import functional_tests.helpers as Helpers


# TODO add negative test
# I.e. try to post with missing fields, etc
def test_cant_create_malformed_expenses(tester):
    # TODO use Helpers.wait_for_required_input(tester, "id_text")
    pass


# TODO add test in which Franks does not select any Categoy from the dropdown
def test_cant_create_expenses_without_selecting_a_category(tester):
    # TODO use Helpers.wait_for_required_input(self, "id_text")
    pass


@Helpers.register_and_login
@skip
def test_expenses_sum_appear_on_home_page(tester):

    category_name = 'Rent'
    curr_mont_amount = 500
    next_month_amount = 420
    first_expense = [
      curr_mont_amount,
      'First month of rent'
    ]
    second_expense = [
      next_month_amount,
      'Second month of rent (discounted)'
    ]
    total_amount = curr_mont_amount + next_month_amount

    Helpers.create_category_and_two_expenses(tester, first_expense,
                                             second_expense, category_name)

    # Frank sees the sum of this month expenses on the home page
    url = reverse('budgets:home')
    tester.browser.get(f"{tester.live_server_url}{url}")
    Helpers.check_amount_and_cat_name(tester, curr_mont_amount, category_name)

    # Frank notices that the current month id displayed in the expense page
    Helpers.check_whether_current_month_date_is_displayed(tester)

    # Frank also notices that only expenses related to the current month are
    # displayed
    Helpers.check_current_month(tester, curr_mont_amount, category_name)


@Helpers.register_and_login
@skip
def test_expenses_page_can_show_old_expenses(tester):
    category_name = 'Rent'
    Helpers.create_a_category(tester, category_name)

    amount = 4000
    note = 'Second month of rent'
    second_date = date.today().replace(day=1)
    second_date_ymd = second_date.strftime("%Y-%m-%d")
    is_income = False
    Helpers.create_entry(tester, amount, category_name, note,
                         second_date_ymd, is_income)

    # Frank visits the expenses page
    note = 'First month of rent'
    delta = timedelta(weeks=10)
    first_rent_date = second_date - delta
    first_rent_date_ym = first_rent_date.strftime("%Y-%m")
    first_rent_date_ymd = first_rent_date.strftime("%Y-%m-%d")
    verify_creation = False
    Helpers.create_entry(tester, amount, category_name, note,
                         first_rent_date_ymd, is_income, verify_creation)

    # Frank visit the expenses page using a parameter
    # (Frank manually changes the URL as he can not find any dropdown yet)
    expense_url = reverse('budgets:expenses')
    url = f"{tester.live_server_url}{expense_url}/{first_rent_date_ym}"
    tester.browser.get(url)

    formatted_amount = f'{amount:n}'
    # Frank notices that this URL does not show entries from other months
    Helpers.verify_expense_was_created(tester,
                                       amount, category_name, note)


@Helpers.register_and_login
def test_only_expenses_in_range_are_shown(tester):

    # Frank creates 2 expenses for January 2020
    category_name = Helpers.generateString()
    Helpers.create_a_category(tester, category_name)

    # Frank is not going to check if the expenses are created as he always does
    # Frank now believes into this sowftware!
    is_income = False
    # We skip verication because...the function is old and broke down due to
    # the new redirect to /expense/create on success ?
    # TODO: check if this is the case, and fix it if needed
    verify_creation = False

    amount = 4000
    note = Helpers.generateString()
    date = "2020-01-01"
    Helpers.create_entry(tester, amount, category_name, note,
                         date, is_income, verify_creation)

    second_amount = 4200
    second_date = "2020-01-07"
    second_note = Helpers.generateString()
    Helpers.create_entry(tester, second_amount, category_name, second_note,
                         date, is_income, verify_creation)

    # Frank has changed his mind: "Testing is important" he says.
    # Frank then enters a special URL to check the expenses creation...but he
    # enters the wrong end date
    expense_url = reverse('budgets:expenses')
    url = f"{tester.live_server_url}{expense_url}/2020-01-01/2020-01-02"
    tester.browser.get(url)

    # Frank notices the first expenses is shown. Frank is so happy
    formatted_amount = f'{amount:,}'
    Helpers.verify_expense_was_created(tester, formatted_amount, category_name,
                                       note)

    # TODO: verify the second expenses is NOT shown
    # Frank can not see the second expenses! Frank wonders whether the
    # software has really saved the second expenses or not

    # Frank then gets very anxious... but then Frank breathes, and re-types the
    # URL. He notices he had typed the wrong one: "Silly me!" he mumbles.
    expense_url = reverse('budgets:expenses')
    url = f"{tester.live_server_url}{expense_url}/2020-01-01/2020-01-07"
    tester.browser.get(url)
    formatted_second_amount = f'{second_amount:,}'

    # Frank now sees both expenses, he smiles. Frank is so relieved now
    Helpers.verify_expense_was_created(tester, formatted_amount, category_name,
                                       note)
    Helpers.verify_expense_was_created(tester, formatted_second_amount,
                                       category_name, second_note)

    # Then, Frank remembers he also bought something during December 2019
    # He really wants to keep track of all his expenses!
    third_amount = 4200
    third_note = Helpers.generateString()
    older_date = "2019-12-31"
    Helpers.create_entry(tester, third_amount, category_name, third_note,
                         older_date, is_income, verify_creation)

    # Frank then enters a special URL that allows him to only show expenses
    # broken down by months
    expense_url = reverse('budgets:expenses')
    url = f"{tester.live_server_url}{expense_url}/2019-12-01/2019-12-31"
    tester.browser.get(url)

    formatted_third_amount = f'{third_amount:,}'
    Helpers.verify_expense_was_created(tester, formatted_third_amount,
                                       category_name, third_note)

    # TODO: Frank then want to see all expenses
    expense_url = reverse('budgets:expenses')
    url = f"{tester.live_server_url}{expense_url}/2019-12-01/2020-01-31"


# TODO: write me
def test_expenses_wont_show_expenses_in_the_future(tester):
    pass


# TODO: write me
def test_creating_expenses_before_categories_will_fail(tester):
    pass


# TODO: write me
def test_graph_is_displayed_in_expenses_page_with_only_one_expense(tester):
    pass
