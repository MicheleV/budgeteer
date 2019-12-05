# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
from django import forms
from budgets.models import Category, Expense, MonthlyBudget
import budgets.models as m


# Docs https://docs.djangoproject.com/en/2.2/ref/forms/
#      fields/#built-in-field-classes
# TODO Look into [1] or [2] to avoid widgets
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

    class Meta:
        def get_choices():
            return m.Category.objects.all()

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
        }


class MonthlyBudgetForm(forms.models.ModelForm):

    class Meta:
        def get_choices():
            return m.Category.objects.all()

        model = m.MonthlyBudget
        fields = ('category', 'amount', 'date')
        widgets = {
          'amount': forms.fields.TextInput(attrs={
              'placeholder': 'Enter the budget amount',
          }),
          'date': forms.fields.TextInput(attrs={
              'placeholder': '%Y-%m-%d format',
          }),
        }

    # Make monthlybudgets be on the first day of the month
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
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a new category of balance (i.e. savings, cash)',
                'class': 'form-control input-lg',
                'autofocus': 'autofocus',
            })
        }


class MonthlyBalanceForm(forms.models.ModelForm):

    class Meta:
        def get_choices():
            return m.MonthlyBalanceCategory.objects.all()

        model = m.MonthlyBalance
        fields = ('category', 'amount', 'date')
        widgets = {
            'amount': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the balance',
            }),
            'date': forms.fields.TextInput(attrs={
                'placeholder': '%Y-%m-%d format',
            }),
        }
