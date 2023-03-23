from django.test import TestCase
from minted.forms import FriendReqForm
from django import forms

class FriendReqFormTest(TestCase):

    def setUp(self):
        self.form_input = {
            'email': 'john@hotmail.co.uk',
            'is_active': 'True',
        }

    def test_form_has_necessary_fields(self):
        form = FriendReqForm()

        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

    def test_valid_friend_req_form(self):
        form = FriendReqForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_empty_email(self):
        self.form_input['email'] = ''
        form = FriendReqForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'bademail'
        form = FriendReqForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        