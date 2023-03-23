from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from minted.forms import PasswordForm
from minted.models import User
from minted.tests.helpers import reverse_with_next

class ChangePasswordViewTest(TestCase):
    """Test suite for the change password view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('change_password')
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123',
        }
        self.user = User.objects.get(pk = 1)
        
    def test_change_password_url(self):
         self.assertEqual(self.url, '/profile/edit/change_password/')

    def test_get_change_password_when_logged_in(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordForm))

    def test_get_change_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_post_change_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_succesful_password_change(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.post(self.url, self.form_input, follow = True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'profile.html')
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 1)
        self.assertEqual(message_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password )
        self.assertTrue(is_password_correct)

    def test_unsuccessful_password_change_due_to_incorrect_current_password(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['password'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_unsuccessful_password_change_due_to_incorrect_password_confirmation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['password_confirmation'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)
