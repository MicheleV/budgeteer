# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime

from django import forms

from budgets.models import Category
from budgets.models import Expense
from budgets.models import MonthlyBudget
import budgets.models as m


# Docs https://docs.djangoproject.com/en/2.2/ref/forms/
#      fields/#built-in-field-classes
# TODO Look into [1] or [2] to avoid widgets
# TODO: do we need to trim the input?
# Credits http://www.obeythetestinggoat.com
# [1] https://django-crispy-forms.readthedocs.org/
# [2] https://django-floppyforms.readthedocs.io/en/latest/
class CategoryForm(forms.models.ModelForm):

    class Meta:
        model = m.Category
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a new category',
                'class': 'form-control input-lg',
                'autofocus': 'autofocus',
            })
        }


class ExpenseForm(forms.models.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = m.Category.objects.filter(created_by=user)

    class Meta:
        model = m.Expense
        fields = ('date', 'amount', 'note', 'category')
        widgets = {
            'amount': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the spended amount',
            }),
            'note': forms.fields.TextInput(attrs={
                'placeholder': 'What did you buy?',
            }),
            'date': forms.fields.TextInput(attrs={
                'placeholder': '%Y-%m-%d format',
            }),
            'category': forms.fields.Select,
        }


class DeleteExpenseForm(forms.models.ModelForm):
    class Meta:
        model = m.Expense
        fields = []


class MonthlyBudgetForm(forms.models.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(MonthlyBudgetForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = m.Category.objects.filter(created_by=user)

    class Meta:
        model = m.MonthlyBudget
        fields = ('category', 'amount', 'date')
        widgets = {
          'amount': forms.fields.TextInput(attrs={
              'placeholder': 'Enter the budget amount',
          }),
          'date': forms.fields.TextInput(attrs={
              'placeholder': '%Y-%m-%d format',
          }),
          'category': forms.fields.Select,
        }

    # On save, make monthlybudgets be on the first day of the month
    def clean(self):
        self.cleaned_data = super(MonthlyBudgetForm, self).clean()
        if 'date' in self.cleaned_data:
            original_date = self.cleaned_data['date']
            final_date = original_date.replace(day=1)
            self.cleaned_data['date'] = final_date
            self.instance.date = final_date
        return self.cleaned_data


class IncomeCategoryForm(forms.models.ModelForm):

    class Meta:
        model = m.IncomeCategory
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a new category',
                'class': 'form-control input-lg',
                'autofocus': 'autofocus',
            })
        }


class IncomeForm(forms.models.ModelForm):

    class Meta:
        model = m.Income
        fields = ('amount', 'note', 'date', 'category')
        widgets = {
            'amount': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the earned amount',
            }),
            'note': forms.fields.TextInput(attrs={
                'placeholder': 'Keyword about this entry',
            }),
            'date': forms.fields.TextInput(attrs={
                'placeholder': '%Y-%m-%d format',
            }),
        }


class MonthlyBalanceCategoryForm(forms.models.ModelForm):

    class Meta:
        model = m.MonthlyBalanceCategory
        fields = ('text', 'is_foreign_currency')
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a new balance category (i.e. savings, ca'
                'sh)',
                'class': 'form-control input-lg',
                'autofocus': 'autofocus',
            }),
            'is_foreign_currency': forms.fields.CheckboxInput(attrs={
              'class': 'form-check-input'
            })
        }


class MonthlyBalanceForm(forms.models.ModelForm):

    class Meta:
        model = m.MonthlyBalance
        fields = ('category', 'amount', 'date')
        widgets = {
            'amount': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the balance',
            }),
            'date': forms.fields.TextInput(attrs={
                'placeholder': '%Y-%m-%d format',
            }),
            # TODO: write a test case to check for autocomplete to be there
            # Workaround for Firefox
            # https://stackoverflow.com/questions/4831848/firefox-ignores-option-selected-selected
            'category': forms.fields.Select(attrs={'autocomplete': 'off'}),
        }


class GoalForm(forms.models.ModelForm):

    class Meta:
        model = m.Goal
        fields = ('amount', 'text', 'note', 'is_archived')
        widgets = {
            'amount': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the amount',
                'class': 'form-control input-lg',
            }),
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Name of the goal (Shows in the graphs)',
                'class': 'form-control input-lg',
                'autofocus': 'autofocus',
            }),
            'note': forms.fields.TextInput(attrs={
                'placeholder': 'Description of what you are trying to achieve',
                'class': 'form-control input-lg',
            }),
            'is_archived': forms.fields.CheckboxInput,
        }
