# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.test import TestCase
from budgets.forms import CategoryForm, ExpenseForm


# Credits http://www.obeythetestinggoat.com/book/chapter_simple_form.html
class CategoryFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CategoryForm()
        self.assertIn('placeholder="Enter a new category"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = CategoryForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
          form.errors['text'],
          ['This field is required.']
        )


class ExpenseFormTest(TestCase):

    def test_form_renders_correctly(self):
        form = ExpenseForm()
        self.assertIn('placeholder="Enter the spended amount"', form.as_p())
        self.assertIn('placeholder="What did you buy?"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())
