from django import forms
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from minted.forms import PasswordForm
from minted.models import User

class PasswordFormTestCase(TestCase):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk = 1)
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123'
        }

    def test_valid_form(self):
        form = PasswordForm(user = self.user, data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = PasswordForm(user = self.user)
        self.assertIn('password', form.fields)
        password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(password_widget, forms.PasswordInput))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_must_contain_user(self):
        form = PasswordForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_be_valid(self):
        self.form_input['password'] = 'WrongPassword123'
        form = PasswordForm(user = self.user, data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = PasswordForm(user = self.user, data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = PasswordForm(user = self.user, data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = PasswordForm(user = self.user, data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = PasswordForm(user = self.user, data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_save_form_changes_password(self):
        form = PasswordForm(user = self.user, data = self.form_input)
        form.full_clean()
        form.save()
        self.user.refresh_from_db()
        self.assertFalse(check_password('Password123', self.user.password))
        self.assertTrue(check_password('NewPassword123', self.user.password))