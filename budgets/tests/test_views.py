# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import resolve
from django.urls import reverse

import budgets.forms as f
from budgets.models import Category
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

    def test_redirect_on_POST(self):
        url = reverse('categories')
        response = self.client.post(url, data={'text': 'Rent'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

    def test_save_on_POST(self):
        url = reverse('new_category')
        response = self.client.post(url,  data={'text': 'Rent'})

        self.assertEqual(Category.objects.count(), 1)
        new_category = Category.objects.first()
        self.assertEqual(new_category.text, 'Rent')

    def test_save_and_retrieve_categories(self):
        first_category = self.create_category('Rent')
        second_category = self.create_category('Food')

        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 2)

        first_saved_category = saved_categories[0]
        second_saved_category = saved_categories[1]
        self.assertEqual(first_saved_category.text, 'Rent')
        self.assertEqual(second_saved_category.text, 'Food')

    def test_create_malformed_categories(self):
        form = f.CategoryForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['This field is required.'])

        form = f.CategoryForm(
          data={'text': 'text longer than constraints!!!!!!!!!!!!!!!!!!!!!!!'})
        self.assertFalse(form.is_valid())
        self.check_if_error_matches('Ensure this value has at most',
                                    form.errors['text'])

    def test_displays_all_categories(self):
        Category.objects.create(text='Rent')
        Category.objects.create(text='Food')

        url = reverse('categories')
        response = self.client.get(url)
        self.assertContains(response, 'Rent')
        self.assertContains(response, 'Food')


class MonthlyBudgetPageTest(BaseTest):

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

    # TODO: write me
    def test_save_and_retrieve_monthly_budget(self):
        pass

    # TODO: write me
    def test_redirect_on_POST(self):
        pass


class ExpensesPageTest(BaseTest):

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('expenses', 'Expenses')

    def test_uses_correct_view(self):
        self.check_if_correct_view('expenses', v.expenses_page)

    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('expenses')
        self.assertTemplateUsed(response, 'expenses.html')

    # TODO
    def test_save_and_retrieve_expenses(self):
        pass

    # TODO
    def test_creating_malformed_expenses_throw_errors(self):
        pass

    def test_creating_expese_before_category_will_fail(self):
        # TODO
        pass

    def test_deleting_categories_witho_attached_expense_will_throw_error(self):
        # NOTE: Atm we do use `on_delete=models.CASCADE` on Expense model,
        # but this test will be necessary in case we do change that
        pass


class IncomeCategoriesPageTest(BaseTest):
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
    # TODO: write me
    def test_redirect_on_POST(self):
        pass

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
