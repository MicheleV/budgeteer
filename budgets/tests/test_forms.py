# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from budgets.forms import CategoryForm, ExpenseForm, MonthlyBudgetForm
from .base import BaseTest


# Credits http://www.obeythetestinggoat.com/book/chapter_simple_form.html
class CategoryFormTest(BaseTest):

    def test_form_renders_correctly(self):
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

    def test_form_validation_length(self):
        text = '----------------text longer than constraints--------------'
        form = CategoryForm(data={'text': text})
        self.assertFalse(form.is_valid())
        self.assertIn(
          'Ensure this value has at most 20 characters',
          form.errors['text'].as_text(),
        )


class ExpenseFormTest(BaseTest):

    def test_form_renders_correctly(self):
        form = ExpenseForm()
        self.assertIn('placeholder="Enter the spended amount"', form.as_p())
        self.assertIn('placeholder="What did you buy?"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    def test_form_validation_category_field(self):
        form = ExpenseForm(data={
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
        form = ExpenseForm(data={
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
        form = ExpenseForm(data={
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
        form = ExpenseForm(data={
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
        form = ExpenseForm(data={
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
        form = MonthlyBudgetForm()
        self.assertIn('placeholder="Enter the budget amount"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    def test_form_validation_category_field(self):
        form = MonthlyBudgetForm(data={
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
        form = MonthlyBudgetForm(data={
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
        form = MonthlyBudgetForm(data={
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
        form = MonthlyBudgetForm(data={
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
        form = MonthlyBudgetForm(data={
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
