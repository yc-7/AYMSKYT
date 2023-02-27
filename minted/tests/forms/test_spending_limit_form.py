from django.test import TestCase
from minted.models import SpendingLimit
from minted.forms import SpendingLimitForm

class SpendingLimitFormTestCase(TestCase):

    def test_valid_spending_limit_form(self):
        input = {'budget': 100, 'timeframe': '/week' }
        form = SpendingLimitForm(data=input)
        self.assertTrue(form.is_valid())

    def test_invalid_spending_limit_form(self):
        input = {'budget': 100.001, 'timeframe': 'week' }
        form = SpendingLimitForm(data=input)
        self.assertFalse(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SpendingLimitForm()
        self.assertIn('budget', form.fields)
        self.assertIn('timeframe', form.fields)