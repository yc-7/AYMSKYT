from django.test import TestCase
from minted.forms import SignUpForm
from minted.models import User
from django import forms

class SignUpFormTest(TestCase):
    """ Test module for SignUpForm """

    def setUp(self):
        self.form_input = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@hotmail.com',
            'new_password': 'Test1234',
            'password_confirmation': 'Test1234',
        }

    def test_valid_form_data(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form has the necessary fields
    def test_form_has_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertEqual(isinstance(email_field, forms.EmailField), True)
        self.assertIn('new_password', form.fields)
        password_field = form.fields['new_password'].widget
        self.assertEqual(isinstance(password_field, forms.PasswordInput), True)
        self.assertIn('password_confirmation', form.fields)
        password_field = form.fields['password_confirmation'].widget
        self.assertEqual(isinstance(password_field, forms.PasswordInput), True)

    # new password must contain an uppercase character
    def test_new_password_must_contain_an_uppercase_character(self):
        self.form_input['new_password'] = 'test1234'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # new password must contain a lowercase character
    def test_new_password_must_contain_a_lowercase_character(self):
        self.form_input['new_password'] = 'TEST1234'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # new password must contain a number
    def test_new_password_must_contain_a_number(self):
        self.form_input['new_password'] = 'TestTest'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # new password and password confirmation must match
    def test_new_password_and_password_confirmation_must_match(self):
        self.form_input['password_confirmation'] = 'badpassword'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    # email must be in the correct format
    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'bademail'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    # email can't be empty   
    def test_form_rejects_empty_email(self):
        self.form_input['email'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    # form can't be empty   
    def test_blank_data(self):
        form = SignUpForm({})
        self.assertFalse(form.is_valid())
