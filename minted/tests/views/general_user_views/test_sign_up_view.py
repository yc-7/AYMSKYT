from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from minted.models import User, SpendingLimit
from minted.forms import SignUpForm, SpendingLimitForm

class SignUpViewTestCase(TestCase):
    """Tests of the sign up view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.url = reverse('sign_up')
        self.spending_input = {
            'budget': '100',
            'timeframe': '/week'
        }
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.user = User.objects.get(pk=1)

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        form = response.context['form']
        spending_form = response.context['spending_form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(isinstance(spending_form, SpendingLimitForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(spending_form.is_bound)
    
    def test_get_sign_up_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unsuccessful_sign_up(self):
        self.form_input['email'] = 'BAD_EMAIL'
        before_count = User.objects.count()
        response = self.client.post(self.url, {**self.spending_input, **self.form_input})
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        spending_form = response.context['spending_form']
        self.assertTrue(isinstance(spending_form, SpendingLimitForm))
        self.assertTrue(spending_form.is_bound)

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, {**self.form_input, **self.spending_input}, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

        user = User.objects.get(email='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertEqual(user.budget.budget, 100.00)
        self.assertEqual(user.budget.timeframe, '/week')