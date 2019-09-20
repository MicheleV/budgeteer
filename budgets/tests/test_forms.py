from django.test import TestCase
from budgets.forms import EMPTY_CATEGORY_ERROR, CategoryForm


# Credits http://www.obeythetestinggoat.com/book/chapter_simple_form.html
class CategoryFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CategoryForm()
        self.assertIn('placeholder="Enter a new category"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = CategoryForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
          form.errors['text'],
          [EMPTY_CATEGORY_ERROR]
        )
