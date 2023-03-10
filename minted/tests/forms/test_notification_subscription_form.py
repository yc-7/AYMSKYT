from django.test import TestCase
from minted.forms import NotificationSubscriptionForm
from django import forms

class NotificationSubscriptionFormTestCase(TestCase):
    fixtures = [
        "minted/tests/fixtures/default_user.json",
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_subscriptions.json",
        "minted/tests/fixtures/default_notification_subscriptions.json"
    ]

    def setUp(self):
        self.form_input = {
            'frequency': 1,
            'subscriptions': [1,2]
        }

    def test_valid_form_data(self):
        form = NotificationSubscriptionForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_fields(self):
        form = NotificationSubscriptionForm()

        self.assertIn('frequency', form.fields)
        frequency_field = form.fields['frequency']
        self.assertTrue(isinstance(frequency_field, forms.TypedChoiceField))

        self.assertIn('subscriptions', form.fields)
        subscriptions_field = form.fields['subscriptions']
        self.assertTrue(isinstance(subscriptions_field, forms.ModelMultipleChoiceField))
    
    def test_form_accepts_empty_frequency(self):
        self.form_input['frequency'] = None
        self._test_form_is_valid()

    def test_form_accepts_empty_subscriptions(self):
        self.form_input['subscriptions'] = None
        self._test_form_is_valid()

    def _test_form_is_valid(self):
        form = NotificationSubscriptionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def _test_form_is_invalid(self):
        form = NotificationSubscriptionForm(data=self.form_input)
        self.assertFalse(form.is_valid())

