# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# TODO: when we''ll have multiple users, we want to expose UUID instead of ID
# in the urls/API
# How to do migrations that include unique fields
# https://docs.djangoproject.com/en/2.2/howto/writing-migrations/#migrations-that-add-unique-fields


class Category(models.Model):
    text = models.CharField(max_length=40, default=None)
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        # Different users can have categories with the same text
        constraints = [
          models.UniqueConstraint(fields=['text', 'created_by'],
                                  name="cat-per-user")
        ]

    def __str__(self):
        return f"{self.text}"


class Expense(models.Model):
    category = models.ForeignKey(Category, default=None, null=True,
                                 on_delete=models.SET_NULL)
    amount = models.IntegerField()
    # Warning: keep in mind this will allow both empty strings AND NULL
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#null
    note = models.CharField(null=True, blank=True, max_length=150, default='')
    date = models.DateField()
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    def __str__(self):
        id = self.category.id
        amount = self.amount
        note = self.note
        date = self.date
        return f"{id}: ({note}), {amount}, {date}"


class MonthlyBudget(models.Model):
    category = models.ForeignKey(Category, default=None, null=True,
                                 on_delete=models.SET_NULL)
    amount = models.IntegerField()
    date = models.DateField()
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('category', 'date')


class IncomeCategory(models.Model):
    text = models.CharField(max_length=40, default=None)
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        # Different users can have monthly balance categories w/ the same text
        constraints = [
          models.UniqueConstraint(fields=['text', 'created_by'],
                                  name="income-cat-per-user")
        ]

    def __str__(self):
        return f"{self.text}"


class Income(models.Model):
    category = models.ForeignKey(IncomeCategory, default=None, null=True,
                                 on_delete=models.SET_NULL)
    amount = models.IntegerField()
    # Warning: keep in mind this will allow both empty strings AND NULL
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#null
    note = models.CharField(null=True, blank=True, max_length=150, default='')
    date = models.DateField()
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    def __str__(self):
        id = self.category.id
        amount = self.amount
        note = self.note
        date = self.date
        return f"{id}: {amount}, {note}, {date}"


class MonthlyBalanceCategory(models.Model):
    text = models.CharField(max_length=40, default=None)
    is_foreign_currency = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        # Different users can have monthly balance categories w/ the same text
        constraints = [
          models.UniqueConstraint(fields=['text', 'created_by'],
                                  name="monthly-balance-cat-per-user")
        ]

    def __str__(self):
        return f"{self.text}"

    def get_absolute_url(self):
        named_url = 'budgets:monthly_balance_categories_details'
        return reverse(named_url, args=[str(self.pk)])


class MonthlyBalance(models.Model):
    category = models.ForeignKey(MonthlyBalanceCategory, default=None,
                                 null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    date = models.DateField()
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    def __str__(self):
        id = self.category.id
        amount = self.amount
        date = self.date
        return f"{id}: {amount}, {date}"

    class Meta:
        # FIXME: unique should be (name + created_by) not only name, as we have
        # multiple users now
        unique_together = ('category', 'date')

    def get_absolute_url(self):
        return reverse('budgets:edit_monthly_balance', args=[str(self.pk)])


class Goal(models.Model):
    amount = models.IntegerField()
    # TODO: unique should be (name + created_by) not only name, as we have
    # multiple users now
    text = models.CharField(max_length=20, default=None, unique=True)
    # FIXME: we do not need note field to be unique
    note = models.CharField(max_length=50, default=None, unique=True)
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, default=None,
                                   null=True, on_delete=models.SET_NULL)

    def __str__(self):
        id = self.id
        amount = self.amount
        text = self.text
        return f"{id}: {amount}, {text}"