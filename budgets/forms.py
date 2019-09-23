# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django import forms

from budgets.models import Category, Expense, MonthlyBudget


# Docs https://docs.djangoproject.com/en/2.2/ref/forms/
#      fields/#built-in-field-classes
# TODO Look into [1] or [2] to avoid widgets
# Credits http://www.obeythetestinggoat.com
# [1] https://django-crispy-forms.readthedocs.org/
# [2] https://django-floppyforms.readthedocs.io/en/latest/
class CategoryForm(forms.models.ModelForm):

    class Meta:
        model = Category
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a new category',
                'class': 'form-control input-lg'
            })
        }


class ExpenseForm(forms.models.ModelForm):

    class Meta:
        model = Expense
        fields = ('amount', 'note', 'spended_date', 'category')
        widgets = {
            'amount': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the spended amount',
            }),
            # TODO note field should NOT be mandatory
            'note': forms.fields.TextInput(attrs={
                'placeholder': 'What did you buy?',
            }),
            'spended_date': forms.fields.TextInput(attrs={
                'placeholder': '%Y-%m-%d format',
            }),
            'category': forms.Select(choices=Category.objects.all())
        }


class MonthlyBudgetForm(forms.models.ModelForm):

    class Meta:
        model = MonthlyBudget
        fields = ('category', 'amount', 'date')
        widgets = {
          'amount': forms.fields.TextInput(attrs={
              'placeholder': 'Enter the budget amount',
          }),
          'date': forms.fields.TextInput(attrs={
              'placeholder': '%Y-%m-%d format',
          }),
          'category': forms.Select(choices=Category.objects.all())
        }
