# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import resolve, reverse
from budgets.views import home_page, categories_page, expenses_page
from budgets.models import Category
from budgets.forms import CategoryForm
from .base import BaseTest


class HomePageTest(BaseTest):

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('home', 'Budgeteer')

    def test_uses_home_view(self):
        self.check_if_correct_view('home', home_page)
        response = self.get_response_from_named_url('expenses')

    def test_uses_home_template(self):
        response = self.get_response_from_named_url('home')
        self.assertTemplateUsed(response, 'home.html')

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

    def test_displays_all_categories(self):
        Category.objects.create(text='Rent')
        Category.objects.create(text='Food')

        url = reverse('categories')
        response = self.client.get(url)
        self.assertContains(response, 'Rent')
        self.assertContains(response, 'Food')


class CategoriesPageTest(BaseTest):

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('categories', 'Categories')

    def test_uses_categories_view(self):
        self.check_if_correct_view('categories', categories_page)

    def test_uses_categories_template(self):
        response = self.get_response_from_named_url('categories')
        self.assertTemplateUsed(response, 'categories.html')

    def test_uses_category_form(self):
        response = self.get_response_from_named_url('categories')
        self.assertIsInstance(response.context['form'], CategoryForm)

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
        form = CategoryForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['This field is required.'])

        form = CategoryForm(
          data={'text': 'text longer than constraints!!!!!!!!!!!!!!!!!!!!!!!'})
        self.assertFalse(form.is_valid())
        self.check_if_error_matches('Ensure this value has at most',
                                    form.errors['text'])


class ExpensesPageTest(BaseTest):

    def test_title_is_displayed(self):
        self.check_if_title_is_displayed('expenses', 'Expenses')

    def test_uses_categories_view(self):
        self.check_if_correct_view('expenses', expenses_page)

    def test_uses_categories_template(self):
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
