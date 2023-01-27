from django.test import TestCase
from PST.forms import LogInForm
from django import forms


class LogInFormTest(TestCase):

    def setUp(self):
        self.form_input = {
            'email': 'john@hotmail.co.uk',
            'password': 'Test1234',
        }

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password'].widget
        self.assertTrue(isinstance(password_field, forms.PasswordInput), True)

    def test_form_is_valid(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = LogInForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_password_field_is_password_field(self):
        form = LogInForm()
        password_field = form.fields['password'].widget
        self.assertTrue(isinstance(password_field, forms.PasswordInput), True)

    def test_form_email_field_is_required(self):
        form = LogInForm()
        email_field = form.fields['email']
        self.assertTrue(email_field.required)

    def test_form_password_field_is_required(self):
        form = LogInForm()
        password_field = form.fields['password']
        self.assertTrue(password_field.required)

    def test_form_email_field_has_correct_label(self):
        form = LogInForm()
        email_field = form.fields['email']
        self.assertEqual(email_field.label, 'Email')

    def test_form_password_field_has_correct_label(self):
        form = LogInForm()
        password_field = form.fields['password']
        self.assertEqual(password_field.label, 'Password')

    # form rejects blank email
    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form rejects blank password
    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form rejects invalid email
    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'bademail'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form rejects invalid password
    def test_form_rejects_invalid_password(self):
        self.form_input['password'] = 'badpassword'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    

   

    


