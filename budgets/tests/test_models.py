# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from budgets.models import Category, Expense
from .base import BaseTest

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
    saved_expenses = Expense.objects.all()
    first_saved_item = saved_expenses[0]
    second_saved_item = saved_expenses[1]

    self.assertEqual(saved_category, category)
    self.assertEqual(saved_expenses.count(), 2)

    self.assertEqual(first_saved_item.category, category)
    self.assertEqual(first_saved_item.amount, 5000)
    self.assertEqual(first_saved_item.note, 'First month of rent')
    self.assertEqual(str(first_saved_item.spended_date), '2019-08-04')

    self.assertEqual(second_saved_item.category, category)
    self.assertEqual(second_saved_item.amount, 4200)
    self.assertEqual(second_saved_item.note, 'Second month of rent (discounted) in advance')
    self.assertEqual(str(second_saved_item.spended_date), '2019-09-04')

  # Credits https://stackoverflow.com/a/24589930
  def test_malformed_categories_triggers_errors(self):
    # None is not allowed
    with transaction.atomic():
      with self.assertRaises(IntegrityError) as e:
        category =  self.create_category(None)
        self.assertEqual(IntegrityError,type(e.exception))

    # Empty strigs are not allowed either
    with transaction.atomic():
      with self.assertRaises(ValidationError) as e:
        category =  self.create_category('')
        self.assertEqual(ValidationError,type(e.exception))

  def test_malformed_expenses_triggers_errors(self):
    category =  self.create_category('Rent')

    # No category
    with transaction.atomic():
      with self.assertRaises(IntegrityError) as e:
        first_expense = self.create_expense(
          category=None,
          amount=5000,
          note='Rent for August 2019',
          spended_date='2019-08-04'
        )
        first_expense.full_clean()
      self.assertEqual(IntegrityError,type(e.exception))

    # amount field: None is not allowed
    with transaction.atomic():
      with self.assertRaises(IntegrityError) as e:
        first_expense = self.create_expense(
          category=category,
          amount=None,
          note='Rent for August 2019',
          spended_date='2019-08-04'
        )
        first_expense.full_clean()
      self.assertEqual(IntegrityError,type(e.exception))

    # note field: None is not allowed
    with transaction.atomic():
      with self.assertRaises(IntegrityError) as e:
        first_expense = self.create_expense(
          category=category,
          amount=5000,
          note=None,
          spended_date='2019-08-04'
        )
        first_expense.full_clean()
      self.assertEqual(IntegrityError,type(e.exception))
    # note field: Empty strigs are not allowed either
    with transaction.atomic():
      with self.assertRaises(ValidationError) as e:
        first_expense = self.create_expense(
          category=category,
          amount=5000,
          note='',
          spended_date='2019-08-04'
        )
        first_expense.full_clean()
      self.assertEqual(ValidationError,type(e.exception))

    # spended_date field: None is not allowed
    with transaction.atomic():
      with self.assertRaises(IntegrityError) as e:
        first_expense = self.create_expense(
          category=category,
          amount=5000,
          note='Rent for August 2019',
          spended_date=None
        )
        first_expense.full_clean()
      self.assertEqual(IntegrityError,type(e.exception))
    # spended_date field: Empty strigs are not allowed either
    with transaction.atomic():
      with self.assertRaises(ValidationError) as e:
        first_expense = self.create_expense(
          category=category,
          amount=5000,
          note='',
          spended_date='2019-08-04'
        )
        first_expense.full_clean()
      self.assertEqual(ValidationError,type(e.exception))