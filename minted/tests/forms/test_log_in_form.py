from django import forms
from django.test import TestCase
from minted.forms import LogInForm

class LogInFormTest(TestCase):
    """Unit tests for the log in form"""

    def setUp(self):
        self.form_input = {'email': 'johndoe@example.org', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_email_field_is_required(self):
        form = LogInForm()
        email_field = form.fields['email']
        self.assertTrue(email_field.required)

    def test_form_email_field_has_correct_label(self):
        form = LogInForm()
        email_field = form.fields['email']
        self.assertEqual(email_field.label, 'Email')

    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = LogInForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_password_field_is_required(self):
        form = LogInForm()
        password_field = form.fields['password']
        self.assertTrue(password_field.required)

    def test_form_password_field_has_correct_label(self):
        form = LogInForm()
        password_field = form.fields['password']
        self.assertEqual(password_field.label, 'Password')

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data = self.form_input)
        self.assertFalse(form.is_valid())

