# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from budgets.models import Category, Expense, MonthlyBudget
from .base import BaseTest


class ModelsTest(BaseTest):

    def test_saving_and_retrieving_expenses(self):
        category = self.create_category('Rent')

        first_expense = self.create_expense(
          category=category,
          amount=5000,
          note='First month of rent',
          spended_date='2019-08-04'
        )
        # Storing the string here to fit into 79 chars limit (PEP8)
        note_field_2 = 'Second month of rent (discounted) in advance'
        second_expense = self.create_expense(
          category=category,
          amount=4200,
          note=note_field_2,
          spended_date='2019-09-04'
        )

        saved_category = Category.objects.first()
        saved_expenses = Expense.objects.all()
        saved_item_1 = saved_expenses[0]
        saved_item_2 = saved_expenses[1]

        self.assertEqual(saved_category, category)
        self.assertEqual(saved_expenses.count(), 2)

        self.assertEqual(saved_item_1.category, category)
        self.assertEqual(saved_item_1.amount, 5000)
        self.assertEqual(saved_item_1.note, 'First month of rent')
        self.assertEqual(str(saved_item_1.spended_date), '2019-08-04')

        self.assertEqual(saved_item_2.category, category)
        self.assertEqual(saved_item_2.amount, 4200)
        self.assertEqual(saved_item_2.note, note_field_2)
        self.assertEqual(str(saved_item_2.spended_date), '2019-09-04')

    # Credits https://stackoverflow.com/a/24589930
    def test_malformed_categories_triggers_errors(self):
        # None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                category = self.create_category(None)
                self.assertEqual(ValidationError, type(e.exception))

        # Empty strigs are not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                category = self.create_category('')
                self.assertEqual(ValidationError, type(e.exception))

        # String longer than 20 chas are not allowed either
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                category = self.create_category(
                  '----------------text longer than constraints--------------')
                self.assertEqual(ValidationError, 'x')

    def test_malformed_expenses_triggers_errors(self):
        category = self.create_category('Rent')

        # No category
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                first_expense = self.create_expense(
                  category=None,
                  amount=5000,
                  note='Rent for August 2019',
                  spended_date='2019-08-04'
                )
                first_expense.full_clean()
            self.assertEqual(ValidationError, type(e.exception))

        # amount field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                first_expense = self.create_expense(
                  category=category,
                  amount=None,
                  note='Rent for August 2019',
                  spended_date='2019-08-04'
                )
                first_expense.full_clean()
            self.assertEqual(ValidationError, type(e.exception))

        # spended_date field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                first_expense = self.create_expense(
                  category=category,
                  amount=5000,
                  note='Rent for August 2019',
                  spended_date=None
                )
                first_expense.full_clean()
            self.assertEqual(ValidationError, type(e.exception))

        # spended_date field: Malformed dates are not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                first_expense = self.create_expense(
                  category=category,
                  amount=5000,
                  note='Rent for August 2019',
                  spended_date='I am a string, not a date!'
                )
                first_expense.full_clean()
            self.assertEqual(ValidationError, type(e.exception))

    def test_saving_and_retrieving_monthly_budgets(self):
        category = self.create_category('Rent')

        first_budget = self.create_monthly_budgets(
          category=category,
          amount=5000,
          date='2019-08-01'
        )
        second_budget = self.create_monthly_budgets(
          category=category,
          amount=4200,
          date='2019-09-01'
        )

        saved_category = Category.objects.first()
        saved_budgets = MonthlyBudget.objects.all()
        first_saved_item = saved_budgets[0]
        second_saved_item = saved_budgets[1]

        self.assertEqual(saved_category, category)
        self.assertEqual(saved_budgets.count(), 2)

        self.assertEqual(first_saved_item.category, category)
        self.assertEqual(first_saved_item.amount, 5000)
        self.assertEqual(str(first_saved_item.date), '2019-08-01')

        self.assertEqual(second_saved_item.category, category)
        self.assertEqual(second_saved_item.amount, 4200)
        self.assertEqual(str(second_saved_item.date), '2019-09-01')

    def test_malformed_monthly_budgets_triggers_errors(self):
        category = self.create_category('Rent')

        # No category
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                budget = self.create_monthly_budgets(
                  category=None,
                  amount=4200,
                  date='2019-09-01'
                )
                budget.full_clean()
            self.assertEqual(ValidationError, type(e.exception))

        # amount field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                budget = self.create_monthly_budgets(
                  category=category,
                  amount=None,
                  date='2019-09-01'
                )
                budget.full_clean()
            self.assertEqual(ValidationError, type(e.exception))

        # date field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                budget = self.create_monthly_budgets(
                  category=category,
                  amount=5000,
                  date=None,
                )
                budget.full_clean()
            self.assertEqual(ValidationError, type(e.exception))
