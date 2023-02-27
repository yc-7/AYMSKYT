from django.test import TestCase
from minted.forms import ExpenditureForm
from minted.models import Expenditure, Category
from django import forms

class ExpenditureFormTestCase(TestCase):

    fixtures = ['minted/tests/fixtures/default_categories.json', 
                'minted/tests/fixtures/default_user.json',
                'minted/tests/fixtures/default_other_user.json',
                "minted/tests/fixtures/default_spending_limit.json"]

    def setUp(self):
        self.form_input = {
            'title': 'Cinema Tickets',
            'price': '30.00',
            'date': '2023-02-25',
            'description': 'Tickets to a movie',
            'receipt_image': None
        }

    def test_valid_form_data(self):
        form = ExpenditureForm(user=1, category='Entertainment', data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_fields(self):
        form = ExpenditureForm(user=1, category='Entertainment')
        self.assertIn('title', form.fields)
        title_field = form.fields['title']
        self.assertTrue(isinstance(title_field, forms.CharField))
        self.assertIn('price', form.fields)
        price_field = form.fields['price']
        self.assertTrue(isinstance(price_field, forms.DecimalField))
        self.assertIn('date', form.fields)
        date_field = form.fields['date']
        date_widget = date_field.widget
        self.assertTrue(isinstance(date_field, forms.DateField))
        self.assertTrue(isinstance(date_widget, forms.DateInput))
        self.assertIn('description', form.fields)
        description_field = form.fields['description']
        description_widget = description_field.widget
        self.assertTrue(isinstance(description_field, forms.CharField))
        self.assertTrue(isinstance(description_widget, forms.Textarea))
        self.assertIn('receipt_image', form.fields)
        receipt_field = form.fields['receipt_image']
        self.assertTrue(isinstance(receipt_field, forms.FileField))
    
    def test_form_rejects_empty_title(self):
        self.form_input['title'] = ''
        self._test_form_is_invalid()
    
    def test_form_rejects_empty_price(self):
        self.form_input['price'] = ''
        self._test_form_is_invalid()
    
    def test_form_rejects_empty_date(self):
        self.form_input['date'] = ''
        self._test_form_is_invalid()
    
    def test_form_accepts_empty_description(self):
        form = ExpenditureForm(user=1, category='Entertainment')
        self.assertEqual(form.fields['description'].required, False)

    def test_form_accepts_empty_receipt_image(self):
        form = ExpenditureForm(user=1, category='Entertainment')
        self.assertEqual(form.fields['receipt_image'].required, False)

    def _test_form_is_valid(self):
        form = ExpenditureForm(user=1, category='Entertainment', data=self.form_input, )
        self.assertTrue(form.is_valid())
    
    def _test_form_is_invalid(self):
        form = ExpenditureForm(user=1, category='Entertainment', data=self.form_input)
        self.assertFalse(form.is_valid())

