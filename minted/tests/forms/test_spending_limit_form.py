from django.test import TestCase
from minted.forms import SpendingLimitForm

class SpendingLimitFormTestCase(TestCase):
    """Unit tests for the spending limit form"""

    def setUp(self):
        self.form_input = {'budget': 100, 'timeframe': '/week'}

    def test_form_contains_required_fields(self):
        form = SpendingLimitForm()
        self.assertIn('budget', form.fields)
        self.assertIn('timeframe', form.fields)

    def test_form_accepts_valid_input(self):
        form = SpendingLimitForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_budget(self):
        self.form_input['budget'] = ''
        form = SpendingLimitForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_3_decimal_places(self):
        self.form_input['budget'] = 100.001
        form = SpendingLimitForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_timeframe(self):
        self.form_input['timeframe'] = ''
        form = SpendingLimitForm(data = self.form_input)
        self.assertFalse(form.is_valid())

