from django.test import TestCase
from django.urls import reverse
from minted.models import User
from minted.forms import SignUpForm
from minted.tests.helpers import LogInTester

class SignUpViewTestCase(TestCase, LogInTester):
    """Tests for the sign up view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('sign_up')
        self.user = User.objects.get(pk = 1)
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/profile')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_get_sign_up_redirects_when_logged_in(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_post_sign_up_redirects_when_logged_in(self):
        self.client.login(email = self.user.email, password = 'Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_successful_sign_up_redirects(self):
        response = self.client.post(self.url, self.form_input, follow = True)
        response_url = reverse('budget_sign_up')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'account/budget_sign_up.html')

    def test_unsuccessful_sign_up(self):
        self.form_input['email'] = 'INVALID_EMAIL'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_sign_up_stores_user_session_data(self):
        response = self.client.post(self.url, self.form_input)
        user_data = response.client.session.get('user_data')
        self.assertEqual(user_data['first_name'], self.form_input['first_name'])
        self.assertEqual(user_data['last_name'], self.form_input['last_name'])
        self.assertEqual(user_data['email'], self.form_input['email'])
        self.assertEqual(user_data['new_password'], self.form_input['new_password'])
        self.assertEqual(user_data['password_confirmation'], self.form_input['password_confirmation'])

