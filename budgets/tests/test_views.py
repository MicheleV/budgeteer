# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
import random

from django.urls import resolve
from django.urls import reverse

import budgets.forms as f
import budgets.models as m
from budgets.tests.base import BaseTest
import budgets.views as v


class HomePageTest(BaseTest):

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('home', 'Budgeteer')

    def test_uses_correct_view(self):
        self.check_if_correct_view('home', v.home_page)
        response = self.get_response_from_named_url('expenses')

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('home')
        self.assertTemplateUsed(response, 'home.html')


class CategoriesPageTest(BaseTest):

    def test_save_on_POST(self):
        url = reverse('categories_create')
        redirect_url = reverse('categories')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})

        self.assertEqual(m.Category.objects.count(), 1)
        new_category = m.Category.objects.first()
        self.assertEqual(new_category.text, text)

    def test_redirect_on_POST(self):
        url = reverse('categories_create')
        redirect_url = reverse('categories')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('categories', 'Categories')

    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('categories', v.categories_page)

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('categories')
        self.assertTemplateUsed(response, 'budgets/category_list.html')

    # def test_uses_category_form(self):
    #     response = self.get_response_from_named_url('categories')
    #     self.assertIsInstance(response.context['form'], f.CategoryForm)

    def test_save_and_retrieve_categories(self):
        text1 = self.generateString(10)
        first_category = self.create_category(text1)
        text2 = self.generateString(10)
        second_category = self.create_category(text2)

        response = self.get_response_from_named_url('categories')
        self.assertContains(response, text1)
        self.assertContains(response, text2)

    def test_displays_all_categories(self):
        text1 = self.generateString(10)
        m.Category.objects.create(text=text1)
        text2 = self.generateString(10)
        m.Category.objects.create(text=text2)

        response = self.get_response_from_named_url('categories')
        self.assertContains(response, text1)
        self.assertContains(response, text2)


class MonthlyBudgetPageTest(BaseTest):

    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_category(text)

        url = reverse('monthly_budgets_create')
        redirect_url = reverse('monthly_budgets')
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

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('monthly_budgets', 'Monthly budgets')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('monthly_budgets', v.monthly_budgets_page)

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('monthly_budgets')
        self.assertTemplateUsed(response, 'budgets/monthlybudget_list.html')

    # def test_uses_category_form(self):
    #     response = self.get_response_from_named_url('monthly_budgets')
    #     self.assertIsInstance(response.context['form'], f.MonthlyBudgetForm)

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

        url = v.append_year_and_month_to_url(mb, 'monthly_budgets')
        response = self.client.get(url)

        self.assertContains(response, text1)
        # Note: we're hardcoding comma as thousand separator in the views
        self.assertContains(response, '{:,}'.format(amount1))
        self.assertContains(response, text2)
        self.assertContains(response, '{:,}'.format(amount2))


class ExpensesPageTest(BaseTest):

    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_category(text)

        url = reverse('expenses_create')
        redirect_url = reverse('expenses')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})
        exp = m.Expense.objects.first()

        url = reverse('expenses_create')
        redirect_url = reverse('expenses')

        self.assertEqual(exp.amount, amount)
        self.assertEqual(exp.date.strftime("%Y-%m-%d"), date)
        self.assertEqual(exp.category.id, cat.id)

        # Merged test_save_and_retrieve_expenses
        view_page = reverse('expenses')
        second_response = self.client.get(view_page)
        # Note: we're hardcoding comma as thousand separator in the views
        self.assertContains(second_response, '{:,}'.format(amount))

        # Merged test_redirect_on_POST(self)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

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
        url = reverse('expenses')
        arg = {'pk': 7}
        response = self.get_response_from_named_url('expenses_delete', arg)
        self.assertEqual(response.status_code, 404)

        # Deletion is successful
        arg = {'pk': expense.id}
        response = self.get_response_from_named_url('expenses_delete', arg)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

        expenses = m.Expense.objects.all()
        self.assertEqual(expenses.count(), 0)

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('expenses', 'Expenses')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('expenses', v.expenses_page)

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('expenses')
        self.assertTemplateUsed(response, 'budgets/expense_list.html')

    def test_delete_button_showed_with_param(self):
        text = self.generateString(10)
        text_2 = self.generateString(10)
        text_3 = self.generateString(10)
        category = self.create_category(text)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        exp = self.create_expense(category, 100, text_2, date)
        exp2 = self.create_expense(category, 100, text_3, date)

        url = f"{reverse('expenses')}?delete=1"
        response = second_response = self.client.get(url)

        delete_form_html = f"form method=\"POST\" action=\"/expenses/delete/{exp.id}\""
        delete_form_html_2 = f"form method=\"POST\" action=\"/expenses/delete/{exp2.id}\""
        button_html = '<input type="submit" id="id_submit" value="Yes, DELETE">'
        self.assertContains(response, delete_form_html)
        self.assertContains(response, delete_form_html_2)
        self.assertContains(response, button_html)

    def test_delete_button_missing_without_param(self):
        text = self.generateString(10)
        text_2 = self.generateString(10)
        category = self.create_category(text)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        exp = self.create_expense(category, 100, text_2, date)

        url = f"{reverse('expenses')}?delete=0"
        response = second_response = self.client.get(url)

        delete_form_html = 'form method="POST" action="/expenses_delete/'
        button_html = '<input type="submit" id="id_submit" value="Yes, DELETE">'
        self.assertNotContains(response, delete_form_html)
        self.assertNotContains(response, button_html)

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


class IncomeCategoriesPageTest(BaseTest):

    def test_save_on_POST(self):
        url = reverse('income_categories_create')
        redirect_url = reverse('income_categories')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        ic = m.IncomeCategory.objects.first()

        self.assertEqual(ic.text, text)

    def test_redirect_on_POST(self):
        url = reverse('income_categories_create')
        redirect_url = reverse('income_categories')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('income_categories',
                                         'Income Categories')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('income_categories',
    #                                v.income_categories_page)
    #     response = self.get_response_from_named_url('income_categories')

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('income_categories')
        self.assertTemplateUsed(response, 'budgets/incomecategory_list.html')


class IncomePageTest(BaseTest):

    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_income_category(text)

        url = reverse('incomes_create')
        redirect_url = reverse('incomes')
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

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('incomes', 'Incomes')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('incomes', v.incomes_page)
    #     response = self.get_response_from_named_url('incomes')

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('incomes')
        self.assertTemplateUsed(response, 'budgets/income_list.html')


class MonthlyBalanceCategoriesTest(BaseTest):

    def test_save_on_POST(self):
        url = reverse('new_monthly_balance_category')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        mb = m.MonthlyBalanceCategory.objects.all()
        self.assertEqual(mb.count(), 1)
        mb = mb.first()
        self.assertEqual(mb.text, text)

    def test_redirect_on_POST(self):
        url = reverse('new_monthly_balance_category')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        redirect_url = reverse('monthly_balance_categories')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    def test_delete_on_POST(self):
        text = self.generateString(10)
        self.create_monthly_balance_category(text)
        new_category = m.MonthlyBalanceCategory.objects.first()
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        mb = self.create_monthly_balance(new_category, 42000, date)

        show_delete = True
        redirect_url = v.append_year_and_month_to_url(mb, 'monthly_balances',
                                                      show_delete)
        arg = {'id': mb.id}
        response = self.get_response_from_named_url('delete_monthly_balance',
                                                    arg)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

        mb = m.MonthlyBalance.objects.all()
        self.assertEqual(mb.count(), 0)

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('monthly_balance_categories',
                                         'Monthly Balance Categories')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('monthly_balance_categories',
    #                                v.MonthlyBalanceCategoryView.as_view())
    #     named_url = 'monthly_balance_categories'
    #     response = self.get_response_from_named_url(named_url)

    def test_uses_correct_template(self):
        named_url = 'monthly_balance_categories'
        response = self.get_response_from_named_url(named_url)
        self.assertTemplateUsed(response, 'budgets/monthlybalancecategory_list.html')


class MonthlyBalanceTest(BaseTest):

    def test_save_and_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_monthly_balance_category(text)

        url = reverse('monthly_balances_create')
        redirect_url = reverse('monthly_balances')
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

    def test_delete_button_showed_with_param(self):
        text = self.generateString(10)
        cat = self.create_monthly_balance_category(text)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1)
        date_ymd = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        date_ym = datetime.date.today().replace(day=1).strftime("%Y-%m")
        mb = self.create_monthly_balance(cat, amount, date_ymd)

        url = f"{reverse('monthly_balances')}/{date_ym}?delete=1"
        response = second_response = self.client.get(url)

        delete_form_html = 'form method="POST" action="/delete_monthly_balance/'
        button_html = '<input type="submit" id="id_submit" value="Yes, DELETE">'
        self.assertContains(response, delete_form_html)
        self.assertContains(response, button_html)

    # TODO: write me
    def test_delete_button_missing_without_param(self):
        pass

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('monthly_balances',
                                         'Monthly Balances')

    # TODO: comment out as we can't compare functions with assertEquals().
    # Need some looking up
    # def test_uses_correct_view(self):
    #     self.check_if_correct_view('monthly_balances', v.monthly_balances_page)
    #     response = self.get_response_from_named_url('monthly_balances')

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('monthly_balances')
        self.assertTemplateUsed(response, 'budgets/monthlybalance_list.html')


class GoalPageTest(BaseTest):
    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('goals',
                                         'Goals')
