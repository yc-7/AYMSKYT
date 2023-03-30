from django import forms
from django.test import TestCase
from minted.forms import FriendReqForm
from minted.models import User

class FriendReqFormTest(TestCase):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_other_user.json",
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk = 1)
        self.form_input = {
            'email': 'janedoe@example.org'
        }

    def test_friend_request_valid_form(self):
        form = FriendReqForm(user = self.user, data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_friend_request_form_has_necessary_fields(self):
        form = FriendReqForm(user = self.user)

        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

    def test_friend_request_form_rejects_empty_email(self):
        self.form_input['email'] = ''
        form = FriendReqForm(user = self.user, data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_friend_request_form_rejects_invalid_email(self):
        self.form_input['email'] = 'BAD_EMAIL'
        form = FriendReqForm(user = self.user, data = self.form_input)
        self.assertFalse(form.is_valid())
        