# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import budgets.forms as f
from .base import BaseTest


# Credits http://www.obeythetestinggoat.com/book/chapter_simple_form.html
class CategoryFormTest(BaseTest):

    def test_form_renders_correctly(self):
        form = f.CategoryForm()
        self.assertIn('placeholder="Enter a new category"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = f.CategoryForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
          form.errors['text'],
          ['This field is required.']
        )

    def test_form_validation_length(self):
        text = '----------------text longer than constraints--------------'
        form = f.CategoryForm(data={'text': text})
        self.assertFalse(form.is_valid())
        self.assertIn(
          'Ensure this value has at most 20 characters',
          form.errors['text'].as_text(),
        )

    def test_autofocus(self):
        form = f.CategoryForm()
        self.assertTrue('autofocus' in str(form))


class IncomeCategoryFormTest(BaseTest):

    def test_form_renders_correctly(self):
        form = f.CategoryForm()
        self.assertIn('placeholder="Enter a new category"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = f.CategoryForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
          form.errors['text'],
          ['This field is required.']
        )

    def test_form_validation_length(self):
        text = '----------------text longer than constraints--------------'
        form = f.CategoryForm(data={'text': text})
        self.assertFalse(form.is_valid())
        self.assertIn(
          'Ensure this value has at most 20 characters',
          form.errors['text'].as_text(),
        )

    def test_autofocus(self):
        form = f.IncomeCategoryForm()
        self.assertTrue('autofocus' in str(form))


# TODO: Write me!
class IncomeFormTest(BaseTest):
    pass


# TODO: Write me!
class MonthlyBalanceCategoryFormTest(BaseTest):
    pass


# TODO: Write me!
class MonthlyBalanceFormTest(BaseTest):
    pass


class ExpenseFormTest(BaseTest):

    def test_form_renders_correctly(self):
        form = f.ExpenseForm()
        self.assertIn('placeholder="Enter the spended amount"', form.as_p())
        self.assertIn('placeholder="What did you buy?"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    def test_form_validation_category_field(self):
        form = f.ExpenseForm(data={
            'category': None,
            'amount': 5000,
            'date': '2019-09-23'
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'category',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )

    def test_form_validation_amount_field(self):
        category = self.create_category('Rent')
        form = f.ExpenseForm(data={
            'category': category.id,
            'amount': None,
            'date': '2019-09-23'
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'amount',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )

    def test_form_validation_date_field(self):
        category = self.create_category('Rent')
        # Case None
        form = f.ExpenseForm(data={
            'category': category.id,
            'amount': 5000,
            'date': None
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )
        # Case empty string
        form = f.ExpenseForm(data={
            'category': category.id,
            'amount': 5000,
            'date': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )
        # Case invalid string
        form = f.ExpenseForm(data={
            'category': category.id,
            'amount': 5000,
            'date': 'I am a string, not a valid date'
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'Enter a valid date',
          form.errors.as_text(),
        )


class MonthlyBudgetFormTest(BaseTest):

    def test_form_renders_correctly(self):
        form = f.MonthlyBudgetForm()
        self.assertIn('placeholder="Enter the budget amount"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    def test_form_validation_category_field(self):
        form = f.MonthlyBudgetForm(data={
            'category': None,
            'amount': 5000,
            'date': '2019-09-23'
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'category',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )

    def test_form_validation_amount_field(self):
        category = self.create_category('Rent')
        form = f.MonthlyBudgetForm(data={
            'category': category.id,
            'amount': None,
            'date': '2019-09-23'
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'amount',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )

    def test_form_validation_date_field(self):
        category = self.create_category('Rent')
        # Case None
        form = f.MonthlyBudgetForm(data={
            'category': category.id,
            'amount': 5000,
            'date': None
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )
        # Case empty string
        form = f.MonthlyBudgetForm(data={
            'category': category.id,
            'amount': 5000,
            'date': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )
        # Case invalid string
        form = f.MonthlyBudgetForm(data={
            'category': category.id,
            'amount': 5000,
            'date': 'I am a string, not a valid date'
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'Enter a valid date',
          form.errors.as_text(),
        )
