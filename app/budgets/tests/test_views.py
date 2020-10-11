# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
from functools import wraps
import random

from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import resolve
from django.urls import reverse

import budgets.forms as f
import budgets.models as m
from budgets.tests.base import BaseTest
import budgets.views as v
import budgets.views_utils as utils


class HomePageTest(BaseTest):
    """Unit tests related to the home page"""

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
        self.check_if_title_is_displayed('budgets:home', 'Budgeteer')

    @BaseTest.login
    def test_uses_correct_view(self):
        self.check_if_correct_view('budgets:home', v.home_page)

    @BaseTest.login
    def test_uses_correct_template(self):
        response = self.get_response_from_named_url('budgets:home')
        self.assertTemplateUsed(response, 'home.html')


class CategoriesPageTest(BaseTest):
    """Unit tests related to the categories pages"""
    @BaseTest.login
    def test_save_on_POST(self):
        url = reverse('budgets:categories_create')
        text = self.generate_string(10)
        self.client.post(url,  data={'text': text})

        self.assertEqual(m.Category.objects.count(), 1)  # pylint: disable=E1101; # noqa
        new_category = m.Category.objects.first()  # pylint: disable=E1101; # noqa
        self.assertEqual(new_category.text, text)

    @BaseTest.login
    def test_redirect_on_POST(self):
        url = reverse('budgets:categories_create')
        redirect_url = reverse('budgets:categories')
        text = self.generate_string(10)

        response = self.client.post(url,  data={'text': text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
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
        """Checks creation and retrieval of categories"""
        text1 = self.generate_string(10)
        self.create_category(text1)
        text2 = self.generate_string(10)
        self.create_category(text2)

        response = self.get_response_from_named_url('budgets:categories')
        self.assertContains(response, text1)
        self.assertContains(response, text2)

    def test_displays_only_current_user_categories(self):
        """Confirm ownership filter works correctly"""

        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()
        text = self.generate_string(10)
        self.create_category(text)

        # Current user: can see it
        response = self.get_response_from_named_url('budgets:categories')
        self.assertContains(response, text)
        self._logout()

        # Create and login as a different user: can't see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:categories')
        self.assertNotContains(response, text)

    @BaseTest.login
    def test_correct_success_url(self):
        """Check if the success_url returned by the view is correct"""
        text = self.generate_string(10)
        url = reverse("budgets:categories_create")
        redirect_url = reverse("budgets:categories")

        # As seen from the client
        response = self.client.post(url,  data={'text': text})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

        # As seen from the View
        url = reverse('budgets:categories_create')
        resolve(url)  # TODO: do we really need this line?

        factory = RequestFactory()
        data = {text: self.generate_string(10)}
        username = self.generate_string(10)
        password = self.generate_string(10)
        request = factory.post(url, data)
        request.user = User.objects.create_user(
            username=username, password=password)
        view = v.CategoryCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(v.CategoryCreateView.get_success_url(request),
                         redirect_url)


class MonthlyBudgetPageTest(BaseTest):

    @BaseTest.login
    def test_save_and_redirect_on_POST(self):
        text = self.generate_string(10)
        cat = self.create_category(text)

        url = reverse('budgets:monthly_budgets_create')
        redirect_url = reverse('budgets:monthly_budgets')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=16).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})
        mb = m.MonthlyBudget.objects.first()  # pylint: disable=E1101; # noqa

        self.assertEqual(mb.amount, amount)
        # Monthly budgets dates have their date set to '1' before being saved
        date_1 = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        self.assertEqual(mb.date.strftime("%Y-%m-%d"), date_1)
        self.assertEqual(mb.category.id, cat.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
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
        text1 = self.generate_string(10)
        cat1 = self.create_category(text1)
        text2 = self.generate_string(10)
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
        """Confirm ownership filter works correctly"""

        # Create and login as a user
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generate_string(10)
        cat = self.create_category(text)

        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        m_b = self.create_monthly_budgets(cat, amount, date)

        # Current user: can see it
        url = reverse('budgets:monthly_budgets')
        response = self.client.get(url)
        self.assertContains(response, text)
        # Note: we're hardcoding comma as thousand separator in the views
        self.assertContains(response, '{:,}'.format(amount))

        self._logout()

        # Create and login as a different user: cant' see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:monthly_budgets')
        self.assertNotContains(response, text)
        self.assertNotContains(response, '{:,}'.format(amount))

    def test_cant_user_other_users_categories_for_monthly_budgets(self):
        """Confirm ownership filter works correctly"""
        # Create and login as a user
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        category_text = self.generate_string(10)
        category = self.create_category(category_text)

        # Current user: can see it
        response = self.get_response_from_named_url('budgets:categories')
        self.assertContains(response, category_text)
        self._logout()

        # Create and login as a different user: cant' see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:categories')
        self.assertNotContains(response, category_text)

        # Note: we redirect to the creation page on success
        redirect_url = url = reverse('budgets:monthly_budgets_create')  # FIXME

        # The second user can't user first user's category
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")

        # The second user can not create monthly budgets using first user's
        # category

        # Obtain reference to the first user's category
        m_b = m.Category.objects.first()  # FIXME: is this used... or needed?
        expected_error_msg = 'Select a valid choice. That choice is not one of the available choices'
        response = self.client.post(url,  data={'amount': amount, 'date': date,
                                    'category': category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_error_msg)


class ExpensesPageTest(BaseTest):

    @BaseTest.login
    def test_save_and_redirect_on_POST(self):
        text = self.generate_string(10)
        cat = self.create_category(text)

        url = reverse('budgets:expenses_create')
        redirect_url = reverse('budgets:expenses')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})  # pylint: disable=E1101; # noqa
        exp = m.Expense.objects.first()  # pylint: disable=E1101; # noqa

        url = reverse('budgets:expenses_create')
        redirect_url = reverse('budgets:expenses_create')
        self.assertEqual(exp.amount, amount)
        self.assertEqual(exp.date.strftime("%Y-%m-%d"), date)
        self.assertEqual(exp.category.id, cat.id)  # pylint: disable=E1101; # noqa

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_delete_expenses(self):
        text = self.generate_string(10)
        text_2 = self.generate_string(10)
        category = self.create_category(text)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        expense = self.create_expense(category, 100, text_2,
                                      date)

        expenses = m.Expense.objects.all()  # pylint: disable=E1101; # noqa
        self.assertEqual(expenses.count(), 1)

        # Delete an unexisting object
        url = reverse('budgets:expenses')
        arg = {'pk': 7}
        response = self.get_response_from_named_url('budgets:expenses_delete', arg)
        self.assertEqual(response.status_code, 404)

        # Deletion is successful
        arg = {'pk': expense.id}  # pylint: disable=E1101; # noqa
        response = self.get_response_from_named_url('budgets:expenses_delete', arg)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)

        expenses = m.Expense.objects.all()  # pylint: disable=E1101; # noqa
        self.assertEqual(expenses.count(), 0)

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
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
        text = self.generate_string(10)
        text_2 = self.generate_string(10)
        text_3 = self.generate_string(10)
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
        text = self.generate_string(10)
        text_2 = self.generate_string(10)
        category = self.create_category(text)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        exp = self.create_expense(category, 100, text_2, date)

        url = f"{reverse('budgets:expenses')}?delete=0"
        response = self.client.get(url)

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
        """Confirm ownership filter works correctly"""

        # Create and login as a user
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        category_text = self.generate_string(10)
        category = self.create_category(category_text)
        note = self.generate_string(10)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        expense = self.create_expense(category=category, amount=amount,
                                      note=note, date=date)

        # Current user: can see it
        response = self.get_response_from_named_url('budgets:expenses')
        self.assertContains(response, category_text)
        self.assertContains(response, note)
        self.assertContains(response, '{:,}'.format(amount))
        self._logout()

        # Create and login as a different user: cant' see it
        self.signup_and_login()
        response = self.get_response_from_named_url('budgets:expenses')
        self.assertNotContains(response, category_text)
        self.assertNotContains(response, note)
        self.assertNotContains(response, '{:,}'.format(amount))

    def test_cant_user_other_users_categories_for_expenses(self):
        """Confirm ownership filter works correctly"""
        # Create and login as a user
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        category_text = self.generate_string(10)
        category = self.create_category(category_text)

        # The first user user can see his category
        response = self.get_response_from_named_url('budgets:categories')
        self.assertContains(response, category_text)
        self._logout()

        # The second user can create a new category
        self.signup_and_login()

        second_category_text = self.generate_string(10)
        second_category = self.create_category(second_category_text)

        # Guido only sees his own category, not Frank's
        response = self.get_response_from_named_url('budgets:categories')
        self.assertNotContains(response, category_text)
        self.assertContains(response, second_category_text)

        # The second user can use his own category to create expenses
        redirect_url = url = reverse('budgets:expenses_create')
        # Note: we redirect to the creation page on success

        amount = random.randint(1, 90000)
        note = self.generate_string(10)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")

        response = self.client.post(url,  data={'amount': amount, 'date': date,
                                    'category': second_category.id, 'note': note})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

        # The second user can not create expenses using the first users's
        # category
        expected_error_msg = 'Select a valid choice. That choice is not one of the available choices'
        response = self.get_response_from_named_url('budgets:expenses')
        self.assertContains(response, note)
        self.assertContains(response, second_category_text)
        self.assertContains(response, '{:,}'.format(amount))

        response = self.client.post(url,  data={'amount': amount, 'date': date,
                                    'category': category.id, 'note': note})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_error_msg)


class IncomeCategoriesPageTest(BaseTest):

    @BaseTest.login
    def test_save_on_POST(self):
        url = reverse('budgets:income_categories_create')
        text = self.generate_string(10)
        self.client.post(url,  data={'text': text})
        i_c = m.IncomeCategory.objects.first()  # pylint: disable=E1101; # noqa

        self.assertEqual(i_c.text, text)

    @BaseTest.login
    def test_redirect_on_POST(self):
        url = reverse('budgets:income_categories_create')
        redirect_url = reverse('budgets:income_categories')
        text = self.generate_string(10)

        response = self.client.post(url,  data={'text': text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
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

        text = self.generate_string(10)
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
        text = self.generate_string(10)
        cat = self.create_income_category(text)

        url = reverse('budgets:incomes_create')
        redirect_url = reverse('budgets:incomes')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})
        inc = m.Income.objects.first()  # pylint: disable=E1101; # noqa
        date = inc.date.strftime('%Y-%m-%d')

        self.assertEqual(inc.amount, amount)
        self.assertEqual(inc.date.strftime("%Y-%m-%d"), date)
        self.assertEqual(inc.category.id, cat.id)

        # Merged test_redirect_on_POST(self)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
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
        """Confirm ownership filter works correctly"""

        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generate_string(10)
        category = self.create_income_category(text)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        note = self.generate_string(10)
        self.create_income(
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

    def test_cant_use_other_users_income_categories_for_income(self):
        """Confirm ownership filter works correctly"""
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generate_string(10)
        category = self.create_income_category(text)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        note = self.generate_string(10)
        income = self.create_income(
          category=category,
          amount=amount,
          note=note,
          date=date
        )

        # First user can see it
        response = self.get_response_from_named_url('budgets:incomes')
        self.assertContains(response, text)
        self.assertContains(response, note)
        self.assertContains(response, '{:,}'.format(amount))

        self._logout()

        # Create and login as another user
        self.signup_and_login()

        # Obtain first user's Income Category details
        income_cat = m.IncomeCategory.objects.first()  # pylint: disable=E1101; # noqa

        # Second user can use his own category to create his own income entry
        second_text = self.generate_string(10)
        second_category = self.create_income_category(second_text)

        second_amount = random.randint(1, 90000)
        second_note = self.generate_string(10)

        second_income = self.create_income(
          category=second_category,
          amount=second_amount,
          note=second_note,
          date=date
        )

        response = self.get_response_from_named_url('budgets:incomes')
        self.assertContains(response, second_note)
        self.assertContains(response, second_text)
        self.assertContains(response, '{:,}'.format(second_amount))

        url = reverse('budgets:incomes_create')

        third_amount = random.randint(1, 90000)
        third_note = self.generate_string(10)

        response = self.client.post(url,  data={'amount': amount, 'date': date,
                                    'category': income_cat.id, 'note': note})

        self.assertEqual(response.status_code, 200)

        # Second user can not create expenses using First user's category
        expected_error_msg = 'Select a valid choice. That choice is not one of the available choices'
        response = self.get_response_from_named_url('budgets:incomes')

        self.assertContains(response, second_note)
        self.assertContains(response, second_text)
        self.assertContains(response, '{:,}'.format(second_amount))

        response = self.client.post(url,  data={'amount': amount, 'date': date,
                                    'category': category.id, 'note': note})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_error_msg)


class MonthlyBalanceCategoriesTest(BaseTest):

    @BaseTest.login
    def test_save_on_POST(self):
        url = reverse('budgets:new_monthly_balance_category')
        text = self.generate_string(10)
        self.client.post(url,  data={'text': text})
        m_b = m.MonthlyBalanceCategory.objects.all()  # pylint: disable=E1101; # noqa
        self.assertEqual(m_b.count(), 1)
        m_b = m_b.first()
        self.assertEqual(m_b.text, text)

    @BaseTest.login
    def test_redirect_on_POST(self):
        url = reverse('budgets:new_monthly_balance_category')
        text = self.generate_string(10)

        # As seen from the client
        response = self.client.post(url,  data={'text': text})
        redirect_url = reverse('budgets:monthly_balance_categories')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

        text = self.generate_string(10)
        self.client.post(url,  data={'text': text})

        response = self.client.post(url,  data={'text': text})
        # TODO: shouldn't it be 302 as above?!
        self.assertEqual(response.status_code, 200)

        # As seen from the View
        resolve(url)

        factory = RequestFactory()
        data = {text: self.generate_string(10)}
        request = factory.post(url, data)
        request.user = self.user

        view = v.MonthlyBalanceCategoryCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(v.MonthlyBalanceCategoryCreateView.get_success_url(request),
                         redirect_url)

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
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
        """Confirm ownership filter works correctly"""

        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generate_string(10)
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
        text = self.generate_string(10)
        cat = self.create_monthly_balance_category(text)

        url = reverse('budgets:monthly_balances_create')
        redirect_url = reverse('budgets:monthly_balances')
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        response = self.client.post(url,  data={'amount': amount,
                                    'date': date, 'category': cat.id})

        exp = m.MonthlyBalance.objects.first()  # pylint: disable=E1101; # noqa
        date = exp.date.strftime('%Y-%m-%d')

        # Merged test_redirect_on_POST(self)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

    # TODO: write me
    def data_is_ordered_by_date_ascending(self):
        pass

    @BaseTest.login
    def test_delete_button_showed_with_param(self):
        text = self.generate_string(10)
        cat = self.create_monthly_balance_category(text)
        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1)
        date_ymd = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        date_ym = datetime.date.today().replace(day=1).strftime("%Y-%m")
        m_b = self.create_monthly_balance(cat, amount, date_ymd)

        url = f"{reverse('budgets:monthly_balances')}/{date_ym}?delete=1"
        response = self.client.get(url)

        form = 'form method="POST" action="/monthly_balances/delete/'
        button = '<input type="submit" id="id_submit" value="Yes, DELETE">'
        self.assertContains(response, form)
        self.assertContains(response, button)

    # TODO: write me
    def test_delete_button_missing_without_param(self):
        pass

    @BaseTest.login
    def test_delete_on_POST(self):
        text = self.generate_string(10)
        self.create_monthly_balance_category(text)
        new_category = m.MonthlyBalanceCategory.objects.first()  # pylint: disable=E1101; # noqa
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        mb = self.create_monthly_balance(new_category, 42000, date)

        show_delete = True
        redirect_url = reverse('budgets:monthly_balances')
        arg = {'pk': mb.id}
        response = self.get_response_from_named_url(
                  'budgets:monthly_balances_delete', arg)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

        mb = m.MonthlyBalance.objects.all()  # pylint: disable=E1101; # noqa
        self.assertEqual(mb.count(), 0)

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
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

    def test_displays_only_current_user_monthly_balances(self):
        """Confirm ownership filter works correctly"""

        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()

        text = self.generate_string(10)
        balance_category = self.create_monthly_balance_category(text)

        amount = random.randint(1, 90000)
        date = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        self.create_monthly_balance(balance_category, amount=amount, date=date)

        # Current user can see it
        # response = self.get_response_from_named_url('budgets:monthly_balances')
        mb = m.MonthlyBalance.objects.first()  # pylint: disable=E1101; # noqa

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

    def test_cant_use_other_uers_balance_categories_for_monthly_balance(self):
        """Confirm ownership filter works correctly"""
        pass


class GoalPageTest(BaseTest):

    @BaseTest.login
    def test_title_is_displayed(self):
        """Check the view title"""
        self.check_if_title_is_displayed('budgets:goals',
                                         'Goals')

    @BaseTest.login
    def test_save_on_POST(self):
        url = reverse('budgets:goals_create')
        text = self.generate_string(10)
        amount = random.randint(1, 90000)
        note = self.generate_string(10)
        self.client.post(url,  data={'text': text, 'amount': amount,
                         'note': note})

        self.assertEqual(m.Goal.objects.count(), 1)  # pylint: disable=E1101; # noqa
        new_goals = m.Goal.objects.first()  # pylint: disable=E1101; # noqa
        self.assertEqual(new_goals.text, text)
        self.assertEqual(new_goals.amount, amount)

    @BaseTest.login
    def test_redirect_on_POST(self):
        url = reverse('budgets:goals_create')
        text = self.generate_string(10)
        note = self.generate_string(10)
        amount = random.randint(1, 90000)
        self.client.post(url,  data={'text': text, 'amount': amount,
                         'note': note})

        response = self.client.post(url,  data={'text': text, 'amount': amount})
        self.assertEqual(response.status_code, 200)

    def test_displays_only_current_user_goals(self):
        """Confirm ownership filter works correctly"""
        # Note: _sign_up() is executed on BaseTest.setUp()
        self._login()
        text = self.generate_string(10)
        note = self.generate_string(10)
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

    @BaseTest.login
    def test_delete_on_POST(self):
        redirect_url = reverse('budgets:goals')
        text = self.generate_string(10)
        note = self.generate_string(10)
        amount = random.randint(1, 90000)

        self.create_goal(amount, text, note)
        new_goal = m.Goal.objects.first()  # pylint: disable=E1101; # noqa

        arg = {'pk': new_goal.id}
        response = self.get_response_from_named_url(
                  'budgets:goals_delete', arg)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

        goals = m.Goal.objects.all()  # pylint: disable=E1101; # noqa
        self.assertEqual(goals.count(), 0)

    @BaseTest.login
    def test_update_on_POST(self):
        text = self.generate_string(10)
        note = self.generate_string(10)
        amount = random.randint(1, 90000)

        self.create_goal(amount, text, note)
        goal = m.Goal.objects.first()  # pylint: disable=E1101; # noqa

        new_text = self.generate_string(10)
        new_note = self.generate_string(10)
        new_amount = random.randint(1, 90000)

        url = reverse('budgets:goals_edit', kwargs={'pk': goal.id})
        response = self.client.post(url, data={'text': new_text,
                                    'amount': new_amount, 'note': new_note})

        redirect_url = reverse('budgets:goals')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], redirect_url)

        goals = m.Goal.objects  # pylint: disable=E1101; # noqa
        self.assertEqual(goals.all().count(), 1)
        updated_goal = goals.first()
        self.assertEqual(updated_goal.text, new_text)
        self.assertEqual(updated_goal.note, new_note)
        self.assertEqual(updated_goal.amount, new_amount)
