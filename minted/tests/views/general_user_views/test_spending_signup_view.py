from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from minted.models import User, SpendingLimit
from minted.forms import SpendingLimitForm, SignUpForm1, SignUpForm2

class SpendingSignupViewTestCase(TestCase):
    """Tests of the sign up view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('spending_signup')
        self.form_input = {
            'budget': '100',
            'timeframe': '/week'
        }
        self.user = User.objects.get(pk=1)

    def test_spending_signup_url(self):
        self.assertEqual(self.url,'/sign_up/spending/')

    def test_get_spending_signup(self):
        session = self.client.session
        session['user_email'] = 'janedoe@example.org'
        session['user_data'] = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        session.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/spending_signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SpendingLimitForm))
        self.assertFalse(form.is_bound)
    
    def test_get_spending_sign_up_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unsuccessful_sign_up(self):
        session = self.client.session
        session['user_email'] = { 'email': 'janedoe@example.org' }
        session['user_data'] = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        session.save()
        self.form_input['budget'] = ''
        before_count = User.objects.count()
        response = self.client.post(self.url, {**self.form_input})
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/spending_signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SpendingLimitForm))
        self.assertTrue(form.is_bound)

    def test_successful_sign_up(self):
        session = self.client.session
        session['user_email'] = { 'email': 'janedoe@example.org' }
        session['user_data'] = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        session.save()
        before_count = User.objects.count()
        response = self.client.post(self.url, {**self.form_input}, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')