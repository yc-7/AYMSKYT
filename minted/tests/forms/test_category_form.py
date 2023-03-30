from django.test import TestCase
from minted.forms import CategoryForm
from django import forms

class CategoryFormTestCase(TestCase):

    fixtures = ['minted/tests/fixtures/default_categories.json', 
            'minted/tests/fixtures/default_spending_limit.json',
            'minted/tests/fixtures/default_user.json',
            'minted/tests/fixtures/default_other_user.json']

    def setUp(self):
        self.form_input = {
            'name': 'Entertainment',
        }
        

    def test_valid_form_data(self):
        form = CategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_fields(self):
        form = CategoryForm(data=self.form_input)
        self.assertIn('name', form.fields)
        name_field = form.fields['name']
        self.assertTrue(isinstance(name_field, forms.CharField))
    
    def test_form_rejects_empty_category_name(self):
        form = CategoryForm(data=self.form_input)
        self.form_input['name'] = ''
        self.assertFalse(form.is_valid())
        