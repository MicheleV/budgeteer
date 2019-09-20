from django import forms

from budgets.models import Category

# TODO move all the errors to a file
# TODO add multilanguage support
EMPTY_CATEGORY_ERROR = "You can't have an empty Category"


class CategoryForm(forms.models.ModelForm):

    class Meta:

        model = Category
        fields = ('text',)
        widget = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a new category',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {'required': EMPTY_CATEGORY_ERROR}
        }

    item_text = forms.CharField(
      widget=forms.fields.TextInput(attrs={
          'placeholder': 'Enter a new category',
          'class': 'form-control input-lg'
        }))
