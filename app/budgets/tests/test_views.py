# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
from functools import wraps
import random

from django.contrib.auth.models import User
from django.urls import resolve
from django.urls import reverse

import budgets.forms as f
import budgets.models as m
from budgets.tests.base import BaseTest
import budgets.views as v
import budgets.views_utils as utils


class HomePageTest(BaseTest):

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:home', 'Budgeteer')

    @BaseTest.login
    def test_uses_correct_view(self):
        self.check_if_correct_view('budgets:home', v.home_page)
        response = self.get_response_from_named_url('budgets:expenses')

    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:home')
        self.assertTemplateUsed(response, 'home.html')


class CategoriesPageTest(BaseTest):

    @BaseTest.login
    def test_save_on_POST(self):
        url = reverse('budgets:categories_create')
        redirect_url = reverse('budgets:categories')
        text = self.generateString(10)

        response = self.client.post(url,  data={'text': text})

        self.assertEqual(m.Category.objects.count(), 1)
        new_category = m.Category.objects.first()
        self.assertEqual(new_category.text, text)

    @BaseTest.login
    def test_redirect_on_POST(self):
        url = reverse('budgets:categories_create')
        redirect_url = reverse('budgets:categories')
        text = self.generateString(10)

        response = self.client.post(url,  data={'text': text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:categories', 'Categories')

    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('categories', v.categories_page)
    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:categories')
        self.assertTemplateUsed(response, 'budgets/category_list.html')

    # def test_uses_category_form(self):
    #     response = self.get_response_from_named_url('budgets:categories')
    #     self.assertIsInstance(response.context['form'], f.CategoryForm)
    @BaseTest.login
    def test_save_and_retrieve_categories(self):
        text1 = self.generateString(10)
        first_category = self.create_category(text1)
        text2 = self.generateString(10)
        second_category = self.create_category(text2)

        response = self.get_response_from_named_url('budgets:categories')
        self.assertContains(response, text1)
        self.assertContains(response, text2)

    @BaseTest.login
    def test_displays_all_categories(self):
        text1 = self.generateString(10)
        m.Category.objects.create(text=text1, created_by=self.user)
        text2 = self.generateString(10)
        m.Category.objects.create(text=text2, created_by=self.user)

        response = self.get_response_from_named_url('budgets:categories')
        self.assertContains(response, text1)
        self.assertContains(response, text2)

    def test_displays_only_current_user_categories(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()
        text = self.generateString(10)
        category = self.create_category(text)

        # Current user can see it
        response = self.get_response_from_named_url('budgets:categories')
        self.assertContains(response, text)
        self._logout()

        # Create and login as a different user: can't see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:categories')
        self.assertNotContains(response, text)


class MonthlyBudgetPageTest(BaseTest):

    @BaseTest.login
    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_category(text)

        url = reverse('budgets:monthly_budgets_create')
        redirect_url = reverse('budgets:monthly_budgets')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=16).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})
        mb = m.MonthlyBudget.objects.first()

        self.assertEqual(mb.amount, amount)
        # Monthly budgets dates have their date set to '1' before being saved
        date_1 = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        self.assertEqual(mb.date.strftime("%Y-%m-%d"), date_1)
        self.assertEqual(mb.category.id, cat.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:monthly_budgets',
                                         'Monthly budgets')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('monthly_budgets', v.monthly_budgets_page)

    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:monthly_budgets')
        self.assertTemplateUsed(response, 'budgets/monthlybudget_list.html')

    # def test_uses_category_form(self):
    #     response = self.get_response_from_named_url('budgets:monthly_budgets')
    #     self.assertIsInstance(response.context['form'], f.MonthlyBudgetForm)
    @BaseTest.login
    def test_save_and_retrieve_monthly_budget(self):
        text1 = self.generateString(10)
        cat1 = self.create_category(text1)
        text2 = self.generateString(10)
        cat2 = self.create_category(text2)

        amount1 = random.randint(1, 90000)
        amount2 = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        mb = self.create_monthly_budgets(cat1, amount1, date)
        mb = self.create_monthly_budgets(cat2, amount2, date)

        url = utils.append_year_and_month_to_url(mb, 'monthly_budgets')
        response = self.client.get(url)

        self.assertContains(response, text1)
        # Note: we're hardcoding comma as thousand separator in the views
        self.assertContains(response, '{:,}'.format(amount1))
        self.assertContains(response, text2)
        self.assertContains(response, '{:,}'.format(amount2))

    def test_displays_only_current_user_monhtly_bugets(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generateString(10)
        cat = self.create_category(text)

        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        mb = self.create_monthly_budgets(cat, amount, date)

        # Current user can see it
        url = view_url = reverse('budgets:monthly_budgets')
        response = self.client.get(url)
        self.assertContains(response, text)
        # Note: we're hardcoding comma as thousand separator in the views
        self.assertContains(response, '{:,}'.format(amount))

        self._logout()

        # Create and login as a different user
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:monthly_budgets')
        self.assertNotContains(response, text)
        self.assertNotContains(response, '{:,}'.format(amount))


class ExpensesPageTest(BaseTest):

    @BaseTest.login
    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_category(text)

        url = reverse('budgets:expenses_create')
        redirect_url = reverse('budgets:expenses')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})
        exp = m.Expense.objects.first()

        url = reverse('budgets:expenses_create')
        redirect_url = reverse('budgets:expenses_create')

        self.assertEqual(exp.amount, amount)
        self.assertEqual(exp.date.strftime("%Y-%m-%d"), date)
        self.assertEqual(exp.category.id, cat.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_delete_expenses(self):
        text = self.generateString(10)
        text_2 = self.generateString(10)
        category = self.create_category(text)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        expense = self.create_expense(category, 100, text_2,
                                      date)

        expenses = m.Expense.objects.all()
        self.assertEqual(expenses.count(), 1)

        # Delete an unexisting object
        url = reverse('budgets:expenses')
        arg = {'pk': 7}
        response = self.get_response_from_named_url('budgets:expenses_delete', arg)
        self.assertEqual(response.status_code, 404)

        # Deletion is successful
        arg = {'pk': expense.id}
        response = self.get_response_from_named_url('budgets:expenses_delete', arg)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

        expenses = m.Expense.objects.all()
        self.assertEqual(expenses.count(), 0)

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:expenses', 'Expenses')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('expenses', v.expenses_page)

    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:expenses')
        self.assertTemplateUsed(response, 'budgets/expense_list.html')

    @BaseTest.login
    def test_delete_button_showed_with_param(self):
        text = self.generateString(10)
        text_2 = self.generateString(10)
        text_3 = self.generateString(10)
        category = self.create_category(text)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        exp = self.create_expense(category, 100, text_2, date)
        exp2 = self.create_expense(category, 100, text_3, date)

        url = f"{reverse('budgets:expenses')}?delete=1"
        response = second_response = self.client.get(url)

        form = f"form method=\"POST\" action=\"/expenses/delete/{exp.id}\""
        form2 = f"form method=\"POST\" action=\"/expenses/delete/{exp2.id}\""
        button = '<input type="submit" id="id_submit" value="Yes, DELETE">'
        self.assertContains(response, form)
        self.assertContains(response, form2)
        self.assertContains(response, button)

    @BaseTest.login
    def test_delete_button_missing_without_param(self):
        text = self.generateString(10)
        text_2 = self.generateString(10)
        category = self.create_category(text)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        exp = self.create_expense(category, 100, text_2, date)

        url = f"{reverse('budgets:expenses')}?delete=0"
        response = second_response = self.client.get(url)

        form = 'form method="POST" action="/expenses_delete/'
        button = '<input type="submit" id="id_submit" value="Yes, DELETE">'
        self.assertNotContains(response, form)
        self.assertNotContains(response, button)

    # TODO
    def test_creating_malformed_expenses_throw_errors(self):
        pass

    def test_creating_expese_before_category_will_fail(self):
        # TODO
        pass

    def test_deleting_categories_without_attached_expense_will_error(self):
        # NOTE: Atm we do use `on_delete=models.CASCADE` on Expense model,
        # but this test will be necessary in case we do change that
        pass

    def test_displays_only_current_user_expenses(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        category_text = self.generateString(10)
        category = self.create_category(category_text)
        note = self.generateString(10)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        expense = self.create_expense(category=category, amount=amount,
                                      note=note, date=date)

        # Current user can see it
        response = self.get_response_from_named_url('budgets:expenses')
        self.assertContains(response, category_text)
        self.assertContains(response, note)
        self.assertContains(response, '{:,}'.format(amount))
        self._logout()

        # Create and login as a different user
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:expenses')
        self.assertNotContains(response, category_text)
        self.assertNotContains(response, note)
        self.assertNotContains(response, '{:,}'.format(amount))


class IncomeCategoriesPageTest(BaseTest):

    @BaseTest.login
    def test_save_on_POST(self):
        url = reverse('budgets:income_categories_create')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        ic = m.IncomeCategory.objects.first()

        self.assertEqual(ic.text, text)

    @BaseTest.login
    def test_redirect_on_POST(self):
        url = reverse('budgets:income_categories_create')
        redirect_url = reverse('budgets:income_categories')
        text = self.generateString(10)

        response = self.client.post(url,  data={'text': text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:income_categories',
                                         'Income Categories')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('income_categories',
    #                                v.income_categories_page)
    #     response = self.get_response_from_named_url('budgets:income_categories')
    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:income_categories')
        self.assertTemplateUsed(response, 'budgets/incomecategory_list.html')

    def test_displays_only_current_user_income_categories(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generateString(10)
        self.create_income_category(text)

        # Current user can see it
        response = self.get_response_from_named_url('budgets:income_categories')
        self.assertContains(response, text)

        self._logout()

        # Create and login as a different user: can't see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:income_categories')
        self.assertNotContains(response, text)


class IncomePageTest(BaseTest):

    @BaseTest.login
    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_income_category(text)

        url = reverse('budgets:incomes_create')
        redirect_url = reverse('budgets:incomes')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})
        inc = m.Income.objects.first()
        date = inc.date.strftime('%Y-%m-%d')

        self.assertEqual(inc.amount, amount)
        self.assertEqual(inc.date.strftime("%Y-%m-%d"), date)
        self.assertEqual(inc.category.id, cat.id)

        # Merged test_redirect_on_POST(self)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:incomes', 'Incomes')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('incomes', v.incomes_page)
    #     response = self.get_response_from_named_url('budgets:incomes')
    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:incomes')
        self.assertTemplateUsed(response, 'budgets/income_list.html')

    def test_displays_only_current_user_income(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generateString(10)
        category = self.create_income_category(text)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        note = self.generateString(10)
        income = self.create_income(
          category=category,
          amount=amount,
          note=note,
          date=date
        )

        # Current user can see it
        response = self.get_response_from_named_url('budgets:incomes')
        self.assertContains(response, text)
        self.assertContains(response, note)
        self.assertContains(response, '{:,}'.format(amount))

        self._logout()

        # Create and login as a different user: can't see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:incomes')
        self.assertNotContains(response, text)
        self.assertNotContains(response, note)
        self.assertNotContains(response, '{:,}'.format(amount))


class MonthlyBalanceCategoriesTest(BaseTest):

    @BaseTest.login
    def test_save_on_POST(self):
        url = reverse('budgets:new_monthly_balance_category')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        mb = m.MonthlyBalanceCategory.objects.all()
        self.assertEqual(mb.count(), 1)
        mb = mb.first()
        self.assertEqual(mb.text, text)

    @BaseTest.login
    def test_redirect_on_POST(self):
        url = reverse('budgets:new_monthly_balance_category')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        redirect_url = reverse('budgets:monthly_balance_categories')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:monthly_balance_categories',
                                         'Monthly Balance Categories')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('monthly_balance_categories',
    #                                v.MonthlyBalanceCategoryView.as_view())
    #     named_url = 'monthly_balance_categories'
    #     response = self.get_response_from_named_url(nbudgets:amed_url)
    @BaseTest.login
    def test_uses_correct_template(self):
        named_url = 'budgets:monthly_balance_categories'
        response = self.get_response_from_named_url(named_url)
        template_name = 'budgets/monthlybalancecategory_list.html'
        self.assertTemplateUsed(response, template_name)

    def test_displays_only_current_monthly_balance_categories(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generateString(10)
        self.create_monthly_balance_category(text)

        # Current user can see it
        response = self.get_response_from_named_url(
                  'budgets:monthly_balance_categories')
        self.assertContains(response, text)

        self._logout()

        # Create and login as a different user: can't see it
        self.signup_and_login()
        response = self.get_response_from_named_url(
          'budgets:monthly_balance_categories')
        self.assertNotContains(response, text)


class MonthlyBalanceTest(BaseTest):

    @BaseTest.login
    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_monthly_balance_category(text)

        url = reverse('budgets:monthly_balances_create')
        redirect_url = reverse('budgets:monthly_balances')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})

        exp = m.MonthlyBalance.objects.first()
        date = exp.date.strftime('%Y-%m-%d')

        # Merged test_redirect_on_POST(self)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    # TODO: write me
    def data_is_ordered_by_date_ascending(self):
        pass

    @BaseTest.login
    def test_delete_button_showed_with_param(self):
        text = self.generateString(10)
        cat = self.create_monthly_balance_category(text)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1)
        date_ymd = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        date_ym = datetime.date.today().replace(day=1).strftime("%Y-%m")
        mb = self.create_monthly_balance(cat, amount, date_ymd)

        url = f"{reverse('budgets:monthly_balances')}/{date_ym}?delete=1"
        response = second_response = self.client.get(url)

        form = 'form method="POST" action="/monthly_balances/delete/'
        button = '<input type="submit" id="id_submit" value="Yes, DELETE">'
        self.assertContains(response, form)
        self.assertContains(response, button)

    # TODO: write me
    def test_delete_button_missing_without_param(self):
        pass

    @BaseTest.login
    def test_delete_on_POST(self):
        text = self.generateString(10)
        self.create_monthly_balance_category(text)
        new_category = m.MonthlyBalanceCategory.objects.first()
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        mb = self.create_monthly_balance(new_category, 42000, date)

        show_delete = True
        redirect_url = reverse('budgets:monthly_balances')
        arg = {'pk': mb.id}
        response = self.get_response_from_named_url(
                  'budgets:monthly_balances_delete', arg)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

        mb = m.MonthlyBalance.objects.all()
        self.assertEqual(mb.count(), 0)

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:monthly_balances',
                                         'Monthly Balances')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #   self.check_if_correct_view('monthly_balances', v.monthly_balances_page)
    #   response = self.get_response_from_named_url('budgets:monthly_balances')

    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:monthly_balances')
        self.assertTemplateUsed(response, 'budgets/monthlybalance_list.html')

    def test_displays_only_current_user_monhtly_balances(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generateString(10)
        balance_category = self.create_monthly_balance_category(text)

        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        self.create_monthly_balance(balance_category, amount=amount, date=date)

        # Current user can see it
        # response = self.get_response_from_named_url('budgets:monthly_balances')
        mb = m.MonthlyBalance.objects.first()

        # Check amount in summary page
        response = self.get_response_from_named_url('budgets:monthly_balances')
        self.assertContains(response, '{:,}'.format(amount))

        url = utils.append_year_and_month_to_url(mb, 'monthly_balances')
        response = self.client.get(url)

        # Check both text and amount in detailed page
        self.assertContains(response, text)
        self.assertContains(response, '{:,}'.format(amount))
        self._logout()

        # Create and login as a different user: can't see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:monthly_balances')
        self.assertNotContains(response, '{:,}'.format(amount))

        url = utils.append_year_and_month_to_url(mb, 'monthly_balances')
        response = self.client.get(url)
        self.assertNotContains(response, text)
        self.assertNotContains(response, '{:,}'.format(amount))
        self._logout()


class GoalPageTest(BaseTest):

    @BaseTest.login
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('budgets:goals',
                                         'Goals')

    def test_displays_only_current_user_goals(self):
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()
        text = self.generateString(10)
        note = self.generateString(10)
        amount = random.randint(1, 90000)
        self.create_goal(amount=amount, text=text, note=note)

        # Current user can see it
        response = self.get_response_from_named_url('budgets:goals')
        self.assertContains(response, text)
        self.assertContains(response, note)
        self.assertContains(response, '{:,}'.format(amount))
        self._logout()

        # Create and login as a different user: can't see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:goals')
        self.assertNotContains(response, text)
        self.assertNotContains(response, note)
        self.assertNotContains(response, '{:,}'.format(amount))
