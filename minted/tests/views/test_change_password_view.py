from django.test import TestCase
from django.urls import reverse
from minted.models import User
from minted.tests.helpers import LogInTester
from django.contrib.auth.forms import PasswordChangeForm


class ChangePasswordViewTestCase(TestCase, LogInTester):
    fixtures = ['minted/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.url = reverse('change_password')
        self.form_input = {
            'old_password': 'Password123',
            'new_password1': 'newPassword123',
            'new_password2': 'newPassword123',
        }
        self.user = User.objects.get(pk = 1)
        
    def test_change_password__url(self):
        self.assertEqual(self.url,'/profile/edit/change_password/')

    def test_get_change_password(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordChangeForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        
    def test_get_change_password_not_logged_in(self):
        response = self.client.get(self.url, follow = True)
        response_url = reverse('log_in') + "?next=" + self.url
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertFalse(self._is_logged_in())  
        
        
    def test_change_password_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PasswordChangeForm)
        response = self.client.post(self.url, self.form_input)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newPassword123'))
        self.assertRedirects(response, '/profile/')
        

        
    def test_change_password_fail(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PasswordChangeForm)
        form_input = {
            'old_password': 'wrong',
            'new_password1': 'newPassword123',
            'new_password2': 'newPassword123',
        }
        response = self.client.post(self.url, form_input)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('newPassword123'))
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        
    def test_change_password_mismatch(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PasswordChangeForm)
        form_input = {
            'old_password': 'Password123',
            'new_password1': 'wrong',
            'new_password2': 'newPassword123',
        }
        response = self.client.post(self.url, form_input)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('newPassword123'))
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        
    
