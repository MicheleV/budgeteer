# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import budgets.forms as f
from .base import BaseTest


# Credits http://www.obeythetestinggoat.com/book/chapter_simple_form.html
class CategoriesTest(BaseTest):
    """
    Categories forms are almost identical, hence we test them all together
    NOTE: when we merge all categories into one model these will break
    """

    def test_autofocus(self):
        """
        Check whether any field has autofocus or not
        """
        forms = [
          f.CategoryForm,
          f.IncomeCategoryForm,
          f.MonthlyBalanceCategoryForm
        ]

        for form in forms:
            self.assertTrue('autofocus' in str(form()))

    def test_form_validation_length(self):
        forms = [
          f.CategoryForm,
          f.IncomeCategoryForm,
          f.MonthlyBalanceCategoryForm
        ]
        text = '----------------text longer than constraints--------------'

        for form in forms:
            filled_form = form(data={'text': text})
            self.assertFalse(filled_form.is_valid())
            self.assertIn(
              'Ensure this value has at most 20 characters',
              filled_form.errors['text'].as_text(),
            )

    # NOTE: we only check for '' string, as users can not input None
    def test_form_validation_for_blank_items(self):
        forms = [
          f.CategoryForm,
          f.IncomeCategoryForm,
          f.MonthlyBalanceCategoryForm
        ]

        for form in forms:
            filled_form = form(data={'text': ''})
            self.assertFalse(filled_form.is_valid())
            self.assertEqual(
              filled_form.errors['text'],
              ['This field is required.']
            )

    def test_form_renders_correctly(self):
        forms = [
          f.CategoryForm,
          f.IncomeCategoryForm,
          # NOTE: MonthlyBalanceCategoryForm has a different placeholder
          #       hence we test it separately below
        ]

        for item in forms:
            form = item()
            self.assertIn('placeholder="Enter a new category"', form.as_p())
            self.assertIn('class="form-control input-lg"', form.as_p())


class MonthlyBalanceCategoryFormTest(BaseTest):

    def test_form_renders_correctly(self):
        form = f.MonthlyBalanceCategoryForm()
        t = 'placeholder="Enter a new category of balance (i.e. savings, cash)'
        self.assertIn(t, form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

# ------------------ end of Categories tests ------------------


# TODO: Write me!
class IncomeFormTest(BaseTest):
    def test_form_renders_correctly(self):
        form = f.IncomeForm()
        self.assertIn('placeholder="Enter the earned amount"', form.as_p())
        self.assertIn('placeholder="Keyword about this entry"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    # TODO: write me
    def test_form_validation_amount_field(self):
        pass

    # TODO: write me
    def test_form_validation_note_field(self):
        pass

    # TODO: write me
    def test_form_validation_date_field(self):
        pass

    # TODO: write me
    def test_form_validation_category_field(self):
        pass


class MonthlyBalanceFormTest(BaseTest):
    def test_form_renders_correctly(self):
        form = f.MonthlyBalanceForm()
        self.assertIn('placeholder="Enter the balance"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    # TODO: write me
    def test_form_validation_text_field(self):
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
