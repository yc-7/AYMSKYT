from django import forms
from django.test import TestCase
from minted.forms import SignUpForm

class SignUpFormTest(TestCase):
    """Unit tests for the sign up form"""

    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }

    def test_form_contains_required_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = SignUpForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'INVALID_EMAIL'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_an_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_a_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_a_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_must_match(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())
