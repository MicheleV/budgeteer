# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
from django import forms
from budgets.models import Category, Expense, MonthlyBudget
from budgets.models import IncomeCategory, Income


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

    # Note
    # def __init__(self, *args, **kwargs):
    #     super(ExpenseForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance:
    #         print(77,instance)
    #         # self.fields['category'] = forms.Select(choices=Category.objects.all())

    class Meta:
        def get_choices():
            # choices = []
            # for choice in Category.objects.all():
            #     choices.append(choice)
            return Category.objects.all()

        def __init__(self, *args, **kwargs):
            super(ExpenseForm, self).__init__(*args, **kwargs)
            self.widgets['category'] = forms.Select(choices=Category.objects.all())

        model = Expense
        fields = ('amount', 'note', 'date', 'category')
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
            # https://github.com/jonashaag/django-addanother/issues/5#issuecomment-196510966
            'category': forms.Select(choices=['a']),
            # 'category': forms.Select(choices=get_choices())
        }


    # TODO uncomment and use this, as soon as views.py uses ExpenseForm
    # def save(self, category):
    #     self.instance.category = category
    #     return super().save()


class MonthlyBudgetForm(forms.models.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ExpenseForm, self).__init__(*args, **kwargs)
    #     self.fields['category'] = forms.Select(choices=get_choices())

    class Meta:
        def get_choices():
            choices = []
            for choice in Category.objects.all():
                choices.append(choice)
            return Category.objects.all()

        model = MonthlyBudget
        fields = ('category', 'amount', 'date')
        widgets = {
          'amount': forms.fields.TextInput(attrs={
              'placeholder': 'Enter the budget amount',
          }),
          'date': forms.fields.TextInput(attrs={
              'placeholder': '%Y-%m-%d format',
          }),
          # 'category': forms.Select(choices=get_choices())
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
        model = IncomeCategory
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a new category',
                'class': 'form-control input-lg'
            })
        }


class IncomeForm(forms.models.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ExpenseForm, self).__init__(*args, **kwargs)
    #     self.fields['category'] = forms.Select(choices=get_choices())

    class Meta:
        model = Income
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
            # 'category': forms.Select(choices=IncomeCategory.objects.all())
        }
