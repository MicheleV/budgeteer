# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import random
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import budgets.forms as f
import budgets.models as m
from budgets.tests.base import BaseTest


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
        text = self.generate_string(50)
        for form in forms:
            filled_form = form(data={'text': text, 'created_by': self.user})

            self.assertFalse(filled_form.is_valid())
            self.assertIn(
              'Ensure this value has at most 40 characters',
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
        t = 'placeholder="Enter a new balance category (i.e. savings, cash)'
        self.assertIn(t, form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

# ------------------ end of Categories tests ------------------


class IncomeFormTest(BaseTest):
    def test_form_renders_correctly(self):
        form = f.IncomeForm(self.user)
        self.assertIn('placeholder="Enter the earned amount"', form.as_p())
        self.assertIn('placeholder="Keyword about this entry"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    def test_form_validation_amount_field(self):
        text = self.generate_string(20)
        category = self.create_income_category(text)
        form = f.IncomeForm(data={
            'category': category.id,
            'amount': None,
            'date': '2019-09-23'
        }, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn(
          'amount',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )

    def test_form_validation_note_field(self):
        text = self.generate_string(20)
        # Note has max length of 150 (set in models.py)
        long_text = self.generate_string(150)
        category = self.create_income_category(text)
        amount = random.randint(1, 90000)
        date = '2020-03-01'
        form = f.IncomeForm(data={
            'category': category.id,
            'amount': amount,
            'date': date,
            'note': long_text
        }, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertNotIn(
          'note',
          form.errors.as_text(),
        )
        self.assertNotIn(
          'Ensure this value has at most',
          form.errors.as_text(),
        )
        # note field can be None
        form = f.IncomeForm(data={
            'category': category.id,
            'amount': amount,
            'date': date,
            'note': None
        }, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertNotIn(
          'note',
          form.errors.as_text(),
        )
        self.assertNotIn(
          'Ensure this value has at most',
          form.errors.as_text(),
        )

    def test_form_validation_date_field(self):
        # Case None
        text = self.generate_string(20)
        category = self.create_income_category(text)
        amount = random.randint(1, 90000)
        form = f.IncomeForm(data={
            'category': category.id,
            'amount': amount,
            'date': None
        }, user=self.user)
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
        form = f.IncomeForm(data={
            'category': category.id,
            'amount': amount,
            'date': ''
        }, user=self.user)
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
            'amount': amount,
            'date': self.generate_string(50)
        }, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'Enter a valid date',
          form.errors.as_text(),
        )

    def test_form_validation_category_field(self):
        amount = random.randint(1, 90000)
        form = f.IncomeForm(data={
            'category': None,
            'amount': amount,
            'date': '2019-09-23'
        }, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn(
          'category',
          form.errors.as_text(),
        )
        self.assertIn(
          'This field is required',
          form.errors.as_text(),
        )


class MonthlyBalanceFormTest(BaseTest):
    def test_form_renders_correctly(self):
        form = f.MonthlyBalanceForm(self.user)
        self.assertIn('placeholder="Enter the balance"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    # TODO: write me
    def test_form_validation_text_field(self):
        pass


class ExpenseFormTest(BaseTest):

    def test_form_renders_correctly(self):
        form = f.ExpenseForm(self.user)
        self.assertIn('placeholder="Enter the spended amount"', form.as_p())
        self.assertIn('placeholder="What did you buy?"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    def test_form_validation_category_field(self):
        form = f.ExpenseForm(data={
            'category': None,
            'amount': 5000,
            'date': '2019-09-23'
        }, user=self.user)
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
        text = self.generate_string(20)
        category = self.create_category(text)
        form = f.ExpenseForm(data={
            'category': category,
            'amount': None,
            'date': '2019-09-23',
        }, user=self.user)
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
        text = self.generate_string(20)
        category = self.create_category(text)
        amount = random.randint(1, 90000)
        # Case None
        form = f.ExpenseForm(data={
            'category': category,
            'amount': amount,
            'date': None,
        }, user=self.user)
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
            'category': category,
            'amount': amount,
            'date': ''
        }, user=self.user)
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
            'category': category,
            'amount': amount,
            'date': self.generate_string(50)
        }, user=self.user)
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
        form = f.MonthlyBudgetForm(self.user)
        self.assertIn('placeholder="Enter the budget amount"', form.as_p())
        self.assertIn('placeholder="%Y-%m-%d format"', form.as_p())

    def test_form_validation_category_field(self):
        form = f.MonthlyBudgetForm(data={
            'category': None,
            'amount': 5000,
            'date': '2019-09-23'
        }, user=self.user)
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
            'date': '2019-09-23',
        }, user=self.user)
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
        amount = random.randint(1, 90000)
        form = f.MonthlyBudgetForm(data={
            'category': category.id,
            'amount': amount,
            'date': None
        }, user=self.user)
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
            'amount': amount,
            'date': ''
        }, user=self.user)
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
            'amount': amount,
            'date': self.generate_string(50),
        }, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn(
          'date',
          form.errors.as_text(),
        )
        self.assertIn(
          'Enter a valid date',
          form.errors.as_text(),
        )

    def test_save_and_update_models(self):
        """
        Test whether the models are saved and updated correctly or not
        """

        amount = random.randint(1, 90000)
        date = '2019-08-01'
        text = self.generate_string(20)
        note = self.generate_string(20)

        amount2 = random.randint(1, 90000)
        date2 = '2019-08-02'
        note2 = self.generate_string(20)
        inc_cat_form = f.IncomeCategoryForm(data={'text': text})
        # NOTE: we need to manually set created_by, as we're not passing through the view logic
        inc_cat_form.instance.created_by = self.user
        inc_cat_form.full_clean()
        inc_cat_form.save()

        saved_income_category = m.IncomeCategory.objects.first()
        self.assertEqual(saved_income_category.text, text)
        self.assertEqual(saved_income_category.created_by.id, self.user.id)

        income_form = f.IncomeForm(data={
            'category': saved_income_category.id,
            'amount': amount,
            'note': note,
            'date': date
        }, user=self.user)

        income_form.full_clean()
        income_form.save()

        saved_income = m.Income.objects.first()
        self.assertEqual(saved_income.amount, amount)
        self.assertEqual(saved_income.note, note)
        self.assertEqual(saved_income.date.strftime("%Y-%m-%d"), date)
        # NOTE: we bypass the view, hence set user is not set

        # Update does not throw errors
        income_form = f.IncomeForm(data={
            'category': saved_income_category.id,
            'amount': amount2,
            'note': note2,
            'date': date2
        }, instance=saved_income, user=self.user)
        income_form.full_clean()
        income_form.save()

        # No new instances were created
        all_incomes = m.Income.objects.all()
        self.assertEqual(len(all_incomes), 1)

        # The update was saved correctly
        updated_income = all_incomes.first()
        self.assertEqual(updated_income.amount, amount2)
        self.assertEqual(updated_income.note, note2)
        self.assertEqual(updated_income.date.strftime("%Y-%m-%d"),
                         date2)
        # NOTE: we bypass the view, hence set user is not set


class GoalFormTest(BaseTest):
    def test_form_renders_correctly(self):
        form = f.GoalForm()
        amount = 'Enter the amount'
        name = 'Name of the goal (Shows in the graphs)'
        text = 'Description of what you are trying to achieve'
        self.assertIn(f'placeholder="{amount}"', form.as_p())
        self.assertIn(f'placeholder="{name}"', form.as_p())
        self.assertIn(f'placeholder="{text}"', form.as_p())

    # TODO: write me
    def test_form_validation_amount_field(self):
        """
        """
        pass

    # TODO: write me
    def test_form_validation_name_field(self):
        """
        """
        pass

    # TODO: write me
    def test_form_validation_text_field(self):
        """
        """
        pass

    def test_save_and_update_models(self):
        """
        Test whether the models are saved and updated correctly or not
        """
        amount = random.randint(1, 90000)
        text = self.generate_string(20)
        note = self.generate_string(20)
        is_archived = False
        goal_form = f.GoalForm(data={
            'amount': amount,
            'text': text,
            'note': note,
            'is_archived': is_archived,
        })
        goal_form.full_clean()
        goal_form.save()

        saved_goal = m.Goal.objects.first()
        self.assertEqual(saved_goal.amount, amount)
        self.assertEqual(saved_goal.text, text)
        self.assertEqual(saved_goal.note, note)
        self.assertEqual(saved_goal.is_archived, is_archived)

        income_form = f.GoalForm(data={
            'amount': amount,
            'text':  text,
            'note': note,
            'is_archived': is_archived
        }, instance=saved_goal)
        income_form.full_clean()
        income_form.save()

        # No new instances were created
        all_goals = m.Goal.objects.all()
        self.assertEqual(len(all_goals), 1)

        # The update was saved correctly
        goal_form = all_goals.first()
        self.assertEqual(goal_form.amount, amount)
        self.assertEqual(goal_form.text, text)
        self.assertEqual(goal_form.note, note)
        self.assertEqual(goal_form.is_archived, is_archived)
