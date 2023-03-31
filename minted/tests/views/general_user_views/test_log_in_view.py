from django.conf import settings
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from minted.forms import LogInForm
from minted.models import User
from minted.tests.helpers import LogInTester, reverse_with_next

class LogInViewTestCase(TestCase, LogInTester):
    """Tests for the log in view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(pk = 1)
        self.admin = User.objects.get(pk = 2)

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_log_in_with_redirect(self):
        destination_url = reverse('create_category')
        self.url = reverse_with_next('log_in', destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(email = self.user.email, password = "Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

    def test_post_log_in_redirects_when_logged_in(self):
        self.client.login(email = self.user.email, password = "Password123")
        form_input = {'email': 'WrongEmail', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input, follow = True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

    def test_post_log_in_with_incorrect_credentials_and_redirect(self):
        redirect_url = reverse('create_category')
        form_input = {'email': self.user.email, 'password': 'WrongPassword123', 'next': redirect_url}
        response = self.client.post(self.url, form_input)
        next = response.context['next']
        self.assertEqual(next, redirect_url)

    def test_successful_log_in(self):
        form_input = {'email': self.user.email, 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER)
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_successful_log_in_for_admin(self):
        form_input = {'email': self.admin.email, 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN)
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'rewards/rewards_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_successful_log_in_with_redirect(self):
        redirect_url = reverse('create_category')
        form_input = {'email': self.user.email, 'password': 'Password123', 'next': redirect_url}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'create_category.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_log_in_is_case_insensitive(self):
        form_input = {'email': 'JOHNDOE@EXAMPlE.ORG', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER)
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_log_in(self):
        form_input = {'email': self.user.email, 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_email(self):
        form_input = {'email': '', 'password': 'Password123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_password(self):
        form_input = {'email': self.user.email, 'password': ''}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {'email': self.user.email, 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
