from django.test import TestCase
from minted.forms import SignUpForm1
from minted.models import User
from django import forms

class SignUpForm1Test(TestCase):
    """ Test module for SignUpForm1 """

    def setUp(self):
        self.form_input = {
            'email': 'test@hotmail.com'
        }

    def test_valid_form_data(self):
        form = SignUpForm1(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_field(self):
        form = SignUpForm1()
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertEqual(isinstance(email_field, forms.EmailField), True)
    
    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'bademail'
        form = SignUpForm1(data=self.form_input)
        self.assertFalse(form.is_valid())
          
    def test_form_rejects_empty_email(self):
        self.form_input['email'] = ''
        form = SignUpForm1(data=self.form_input)
        self.assertFalse(form.is_valid())