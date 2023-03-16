from django.test import TestCase
from minted.models import User
from minted.forms import NewPasswordForm
from django.contrib.auth.hashers import check_password

class NewPasswordFormTestCase(TestCase):
    """Test suite for new password form - password resets"""
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', password='TestPassword123')
        self.form_input = {
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_valid_form(self):
        form = NewPasswordForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        self.form_input['password_confirmation'] = 'NOT_NEW_PASSWORD'
        form = NewPasswordForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['password_confirmation'])

    def test_form_saves_correctly(self):
        form = NewPasswordForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        
        self.user.refresh_from_db()
        is_password_correct = check_password(self.form_input['new_password'], self.user.password)
        self.assertTrue(is_password_correct)