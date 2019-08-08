# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest

from budgets.views import home_page, categories_page
from budgets.models import Category, Expense

class BaseTest(TestCase):

  def create_category(self, text):
    category = Category()
    category.text = text
    category.save()
    return category

  def create_expense(self, category, amount, note, spended_date):
    first_expense = Expense()
    first_expense.category = category
    first_expense.amount = amount
    first_expense.note = note
    first_expense.spended_date = spended_date
    first_expense.save()
    return first_expense

  def get_response_from_named_url(self, named_url):
    url = reverse(named_url)
    response = self.client.get(url)
    return response

class HomePageTest(BaseTest):

  def test_title_is_displayed(self):
    url = reverse('home')
    response = self.client.get(url)
    self.assertContains(response,'Budgeteer')

  def test_uses_home_view(self):
    url = reverse('home')
    found = resolve(url)
    self.assertEqual(found.func, home_page)

  def test_uses_home_template(self):
    url = reverse('home')
    response = self.client.get(url)
    self.assertTemplateUsed(response, 'home.html')

  def test_redirect_on_POST(self):
    url = reverse('categories')
    response = self.client.post(url,  data={'category_text': 'Rent'})
    self.assertEqual(response.status_code,302)
    self.assertEqual(response['location'],url)

  def test_save_on_POST(self):
    url = reverse('new_category')
    response = self.client.post(url,  data={'category_text': 'Rent'})

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
    response = self.get_response_from_named_url('categories')
    self.assertContains(response,'Categories')

  def test_uses_categories_view(self):
    url = reverse('categories')
    found = resolve(url)
    self.assertEqual(found.func, categories_page)

  def test_uses_categories_template(self):
    response = self.get_response_from_named_url('categories')
    self.assertTemplateUsed(response, 'categories.html')

  def test_save_and_retrieve_categories(self):
    first_category = self.create_category('Rent')
    second_category = self.create_category('Food')

    saved_categories = Category.objects.all()
    self.assertEqual( saved_categories.count(), 2)

    first_saved_category = saved_categories[0]
    second_saved_category = saved_categories[1]
    self.assertEqual(first_saved_category.text, 'Rent')
    self.assertEqual(second_saved_category.text, 'Food')

class ModelsTest(BaseTest):

  def test_saving_and_retrieving_expenses(self):
    category =  self.create_category('Rent')

    first_expense = self.create_expense(
      category=category,
      amount=5000,
      note='First month of rent',
      spended_date='2019-08-04'
    )

    second_expense = self.create_expense(
      category=category,
      amount=4200,
      note='Second month of rent (discounted) in advance',
      spended_date='2019-09-04'
    )

    saved_category = Category.objects.first()
    self.assertEqual(saved_category, category)
    saves_expenses = Expense.objects.all()
    self.assertEqual(saves_expenses.count(), 2)
    first_saved_item = saves_expenses[0]
    second_saved_item = saves_expenses[1]

    self.assertEqual(first_saved_item.category, category)
    self.assertEqual(first_saved_item.amount, 5000)
    self.assertEqual(first_saved_item.note, 'First month of rent')
    self.assertEqual(str(first_saved_item.spended_date), '2019-08-04')

    self.assertEqual(second_saved_item.category, category)
    self.assertEqual(second_saved_item.amount, 4200)
    self.assertEqual(second_saved_item.note, 'Second month of rent (discounted) in advance')
    self.assertEqual(str(second_saved_item.spended_date), '2019-09-04')
