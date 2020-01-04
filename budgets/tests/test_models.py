# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.db import transaction
from django.db.utils import IntegrityError

from django.core.exceptions import ValidationError

import budgets.models as m
from budgets.tests.base import BaseTest


class ModelsTest(BaseTest):

    def test_saving_and_retrieving_expenses(self):
        category = self.create_category('Rent')

        first_expense = self.create_expense(
          category=category,
          amount=5000,
          note='First month of rent',
          date='2019-08-04'
        )
        # Storing the string here to fit into 79 chars limit (PEP8)
        note_field_2 = 'Second month of rent (discounted) in advance'
        second_expense = self.create_expense(
          category=category,
          amount=4200,
          note=note_field_2,
          date='2019-09-04'
        )

        saved_category = m.Category.objects.first()
        saved_expenses = m.Expense.objects.all()
        saved_item_1 = saved_expenses[0]
        saved_item_2 = saved_expenses[1]

        self.assertEqual(saved_category, category)
        self.assertEqual(saved_expenses.count(), 2)

        self.assertEqual(saved_item_1.category, category)
        self.assertEqual(saved_item_1.amount, 5000)
        self.assertEqual(saved_item_1.note, 'First month of rent')
        self.assertEqual(str(saved_item_1.date), '2019-08-04')

        self.assertEqual(saved_item_2.category, category)
        self.assertEqual(saved_item_2.amount, 4200)
        self.assertEqual(saved_item_2.note, note_field_2)
        self.assertEqual(str(saved_item_2.date), '2019-09-04')

    def test_saving_and_retrieving_income(self):
        category = self.create_income_category('Rent')
        first_income = self.create_income(
          category=category,
          amount=10000,
          note='August Wage',
          date='2019-08-10'
        )
        second_income = self.create_income(
          category=category,
          amount=30000,
          note='September Wage',
          date='2019-09-10'
        )

        saved_category = m.IncomeCategory.objects.first()
        saved_expenses = m.Income.objects.all()
        saved_item_1 = saved_expenses[0]
        saved_item_2 = saved_expenses[1]

        self.assertEqual(saved_category, category)
        self.assertEqual(saved_expenses.count(), 2)

        self.assertEqual(saved_item_1.category, category)
        self.assertEqual(saved_item_1.amount, 10000)
        self.assertEqual(saved_item_1.note, 'August Wage')
        self.assertEqual(str(saved_item_1.date), '2019-08-10')

        self.assertEqual(saved_item_2.category, category)
        self.assertEqual(saved_item_2.amount, 30000)
        self.assertEqual(saved_item_2.note, 'September Wage')
        self.assertEqual(str(saved_item_2.date), '2019-09-10')

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
            self.assertEqual(ValidationError, type(e.exception))

    def test_duplicates_categories_triggers_errors(self):
        category = self.create_category('Rent')
        with self.assertRaises(ValidationError) as e:
            category = self.create_category('Rent')

    def test_malformed_income_categories_triggers_errors(self):
        # None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                category = self.create_income_category(None)
            self.assertEqual(ValidationError, type(e.exception))

        # Empty strigs are not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                category = self.create_income_category('')
            self.assertEqual(ValidationError, type(e.exception))

        # String longer than 20 chas are not allowed either
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                category = self.create_income_category(
                  '----------------text longer than constraints--------------')
            self.assertEqual(ValidationError, type(e.exception))

    def test_duplicates_income_categories_triggers_errors(self):
        category = self.create_income_category('Wage')
        with self.assertRaises(ValidationError) as e:
            category = self.create_income_category('Wage')

    def test_malformed_expenses_triggers_errors(self):
        category = self.create_category('Rent')

        # No category
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                expense = self.create_expense(
                  category=None,
                  amount=5000,
                  note='Rent for August 2019',
                  date='2019-08-04'
                )
            self.assertEqual(ValidationError, type(e.exception))

        # amount field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                expense = self.create_expense(
                  category=category,
                  amount=None,
                  note='Rent for August 2019',
                  date='2019-08-04'
                )
            self.assertEqual(ValidationError, type(e.exception))

        # date field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                expense = self.create_expense(
                  category=category,
                  amount=5000,
                  note='Rent for August 2019',
                  date=None
                )
            self.assertEqual(ValidationError, type(e.exception))

        # date field: Malformed dates are not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                expense = self.create_expense(
                  category=category,
                  amount=5000,
                  note='Rent for August 2019',
                  date='I am a string, not a date!'
                )
            self.assertEqual(ValidationError, type(e.exception))

    def test_malformed_income_triggers_errors(self):
        category = self.create_income_category('Wage')

        # No category
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                income = self.create_income(
                  category=None,
                  amount=10000,
                  note='Wage for August 2019',
                  date='2019-08-01'
                )
            self.assertEqual(ValidationError, type(e.exception))

        # amount field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                income = self.create_income(
                  category=category,
                  amount=None,
                  note='Wage for August 2019',
                  date='2019-08-01'
                )
            self.assertEqual(ValidationError, type(e.exception))

        # date field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                income = self.create_income(
                  category=category,
                  amount=10000,
                  note='Wage for August 2019',
                  date=None
                )
            self.assertEqual(ValidationError, type(e.exception))

        # date field: Malformed dates are not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                income = self.create_income(
                  category=category,
                  amount=10000,
                  note='Rent for August 2019',
                  date='I am a string, not a date!'
                )
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

        saved_category = m.Category.objects.first()
        saved_budgets = m.MonthlyBudget.objects.all()
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
            self.assertEqual(ValidationError, type(e.exception))

        # amount field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                budget = self.create_monthly_budgets(
                  category=category,
                  amount=None,
                  date='2019-09-01'
                )
            self.assertEqual(ValidationError, type(e.exception))

        # date field: None is not allowed
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                budget = self.create_monthly_budgets(
                  category=category,
                  amount=5000,
                  date=None,
                )
            self.assertEqual(ValidationError, type(e.exception))

    def test_duplicates_monthly_budget_triggers_errors(self):
        category = self.create_category('Rent')

        monthly_budget = self.create_monthly_budgets(
          category=category,
          amount=4200,
          date='2019-09-01'
        )

        # Duplicate
        with transaction.atomic():
            with self.assertRaises(ValidationError) as e:
                monthly_budget = self.create_monthly_budgets(
                  category=category,
                  amount=4200,
                  date='2019-09-01'
                )
            self.assertEqual(ValidationError, type(e.exception))

    # TODO: Write me!
    def test_saving_and_retrieving_monthly_balance_categories(self):
        pass

    # TODO: Write me!
    def test_malformed_monthly_balance_categories_triggers_errors(self):
        pass

    # TODO: Write me!
    def test_duplicates_monthly_balance_categories_triggers_errors(self):
        pass

    # TODO: Write me!
    def test_saving_and_retrieving_monthly_balance(self):
        pass

    # TODO: Write me!
    def test_malformed_monthly_balance_triggers_errors(self):
        pass

    # TODO: Write me!
    def test_duplicates_monthly_balances_triggers_errors(self):
        pass
