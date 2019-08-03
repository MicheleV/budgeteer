# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.urls import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest

from budgets.views import home_page, categories_page

class HomePageTest(TestCase):

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

class CategoriesPageTest(TestCase):

  def test_title_is_displayed(self):
    url = reverse('categories')
    response = self.client.get(url)
    self.assertContains(response,'Categories')

  def test_uses_categories_view(self):
    url = reverse('categories')
    found = resolve(url)
    self.assertEqual(found.func, categories_page)

  def test_uses_home_template(self):
    url = reverse('categories')
    response = self.client.get(url)
    self.assertTemplateUsed(response, 'categories.html')

