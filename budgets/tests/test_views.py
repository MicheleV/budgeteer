# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
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
        url = reverse('new_category')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})

        self.assertEqual(m.Category.objects.count(), 1)
        new_category = m.Category.objects.first()
        self.assertEqual(new_category.text, text)

    def test_redirect_on_POST(self):
        url = reverse('categories')
        text = self.generateString(10)
        response = self.client.post(url, data={'text': text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('categories', 'Categories')

    def test_uses_correct_view(self):
        self.check_if_correct_view('categories', v.categories_page)

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('categories')
        self.assertTemplateUsed(response, 'categories.html')

    def test_uses_category_form(self):
        response = self.get_response_from_named_url('categories')
        self.assertIsInstance(response.context['form'], f.CategoryForm)

    def test_save_and_retrieve_categories(self):
        text1 = self.generateString(10)
        first_category = self.create_category(text1)
        text2 = self.generateString(10)
        second_category = self.create_category(text2)

        saved_categories = m.Category.objects.all()
        self.assertEqual(saved_categories.count(), 2)

        first_saved_category = saved_categories[0]
        self.assertEqual(first_saved_category.text, text1)
        second_saved_category = saved_categories[1]
        self.assertEqual(second_saved_category.text, text2)

    def test_create_malformed_categories(self):
        form = f.CategoryForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['This field is required.'])

        long_string = self.generateString(50)
        form = f.CategoryForm(
          data={'text': long_string})
        self.assertFalse(form.is_valid())
        self.check_if_error_matches('Ensure this value has at most',
                                    form.errors['text'])

    def test_displays_all_categories(self):
        text1 = self.generateString(10)
        m.Category.objects.create(text=text1)
        text2 = self.generateString(10)
        m.Category.objects.create(text=text2)

        url = reverse('categories')
        response = self.client.get(url)
        self.assertContains(response, text1)
        self.assertContains(response, text2)


class MonthlyBudgetPageTest(BaseTest):

    def test_save_on_POST(self):
        text = self.generateString(10)
        cat = self.create_category(text)
        url = reverse('new_monthly_budget')
        amount = random.randint(1, 90000)
        response = self.client.post(url,  data={'amount': amount,
                                    'date': '2020-02-16', 'category': cat.id})
        mb = m.MonthlyBudget.objects.first()
        self.assertEqual(mb.amount, amount)
        date = mb.date.strftime('%Y-%m-%d')
        # Monthly budgets dates have their date set to '1' before being saved
        self.assertEqual('2020-02-01', date)
        self.assertEqual(mb.category.id, cat.id)

    def test_redirect_on_POST(self):
        text = self.generateString(10)
        cat = self.create_category(text)
        url = reverse('new_monthly_budget')
        amount = random.randint(1, 90000)
        response = self.client.post(url,  data={'amount': amount,
                                    'date': '2020-02-16', 'category': cat.id})
        url = reverse('monthly_balance_categories')
        response = self.client.post(url,  data={'text': 'Account #1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('monthly_budgets', 'Monthly budgets')

    def test_uses_correct_view(self):
        self.check_if_correct_view('monthly_budgets', v.monthly_budgets_page)

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('monthly_budgets')
        self.assertTemplateUsed(response, 'monthly_budgets.html')

    def test_uses_category_form(self):
        response = self.get_response_from_named_url('monthly_budgets')
        self.assertIsInstance(response.context['form'], f.MonthlyBudgetForm)

    # TODO
    def test_delete_button_showed_with_param(self):
        pass

    # TODO
    def test_delete_button_missing_without_param(self):
        pass

    # TODO: write me
    def test_save_and_retrieve_monthly_budget(self):
        pass


class ExpensesPageTest(BaseTest):

    # TODO: write me
    def test_save_on_POST(self):
        pass

    # TODO: write me
    def test_redirect_on_POST(self):
        pass

    def test_delete_expenses(self):
        text = self.generateString(10)
        category = self.create_category(text)
        expense = self.create_expense(category, 100, 'An expense',
                                      '2020-01-01')

        expenses = m.Expense.objects.all()
        self.assertEqual(expenses.count(), 1)

        # Delete an unexisting object
        url = reverse('expenses')
        arg = {'id': 7}
        response = self.get_response_from_named_url('delete_expense', arg)
        self.assertEqual(response.status_code, 404)

        # Deletion is successful
        arg = {'id': expense.id}
        response = self.get_response_from_named_url('delete_expense', arg)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

        expenses = m.Expense.objects.all()
        self.assertEqual(expenses.count(), 0)

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('expenses', 'Expenses')

    def test_uses_correct_view(self):
        self.check_if_correct_view('expenses', v.expenses_page)

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('expenses')
        self.assertTemplateUsed(response, 'expenses.html')

    # TODO
    def test_delete_button_showed_with_param(self):
        pass

    # TODO
    def test_delete_button_missing_without_param(self):
        pass

    # TODO
    def test_save_and_retrieve_expenses(self):
        pass

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
    # TODO: write me
    def test_save_on_POST(self):
        pass

    # TODO: write me
    def test_redirect_on_POST(self):
        pass

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('income_categories',
                                         'Income Categories')

    def test_uses_correct_view(self):
        self.check_if_correct_view('income_categories',
                                   v.income_categories_page)
        response = self.get_response_from_named_url('income_categories')

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('income_categories')
        self.assertTemplateUsed(response, 'income_categories.html')


class IncomePageTest(BaseTest):

    # TODO: write me
    def test_save_on_POST(self):
        pass

    # TODO: write me
    def test_redirect_on_POST(self):
        pass

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('incomes', 'Incomes')

    def test_uses_correct_view(self):
        self.check_if_correct_view('incomes', v.incomes_page)
        response = self.get_response_from_named_url('incomes')

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('incomes')
        self.assertTemplateUsed(response, 'incomes.html')


class MonthlyBalanceCategoriesTest(BaseTest):

    def test_save_on_POST(self):
        url = reverse('monthly_balance_categories')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        mb = m.MonthlyBalanceCategory.objects.all()
        self.assertEqual(mb.count(), 1)
        mb = mb.first()
        self.assertEqual(mb.text, text)

    def test_redirect_on_POST(self):
        url = reverse('monthly_balance_categories')
        text = self.generateString(10)
        response = self.client.post(url,  data={'text': text})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

    def test_delete_on_POST(self):
        text = self.generateString(10)
        self.create_monthly_balance_category(text)
        new_category = m.MonthlyBalanceCategory.objects.first()
        mb = self.create_monthly_balance(new_category, 42000, '2020-02-16')

        show_delete = True
        redirect_url = v.create_url_for_monthly_budget(mb, show_delete)
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

    def test_uses_correct_view(self):
        self.check_if_correct_view('monthly_balance_categories',
                                   v.monthly_balance_categories_page)
        named_url = 'monthly_balance_categories'
        response = self.get_response_from_named_url(named_url)

    def test_uses_correct_template(self):
        named_url = 'monthly_balance_categories'
        response = self.get_response_from_named_url(named_url)
        self.assertTemplateUsed(response, 'monthly_balance_categories.html')


class MonthlyBalanceTest(BaseTest):

    # TODO: write me
    def test_save_on_POST(self):
        pass

    # TODO: write me
    def test_redirect_on_POST(self):
        pass

    # TODO: write me
    def test_delete_on_POST(self):
        pass

    # TODO: write me
    def test_redirect_on_delete_POST(self):
        pass

    # TODO: write me
    def data_is_ordered_by_date_ascending(self):
        pass

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('monthly_balances',
                                         'Monthly Balances')

    def test_uses_correct_view(self):
        self.check_if_correct_view('monthly_balances', v.monthly_balances_page)
        response = self.get_response_from_named_url('monthly_balances')

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('monthly_balances')
        self.assertTemplateUsed(response, 'monthly_balances.html')
