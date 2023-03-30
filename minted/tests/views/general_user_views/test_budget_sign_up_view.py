from django.test import TestCase
from django.urls import reverse
from minted.models import User
from minted.forms import SpendingLimitForm
from minted.tests.helpers import LogInTester

class BudgetSignupViewTestCase(TestCase, LogInTester):
    """Tests of the budget sign up view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('budget_sign_up')
        self.user = User.objects.get(pk = 1)
        self.form_input = {
            'budget': '100',
            'timeframe': '/week'
        }
        self.session = self.client.session
        self.session['user_data'] = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_budget_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/budget/')

    def test_get_budget_sign_up(self):
        self.session.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/budget_sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SpendingLimitForm))
        self.assertFalse(form.is_bound)
    
    def test_get_budget_sign_up_redirects_when_logged_in(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_post_budget_sign_up_redirects_when_logged_in(self):
        self.client.login(email = self.user.email, password = 'Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard.html')
    
    def test_get_budget_sign_up_redirects_with_no_user_data(self):
        self.session['user_data'] = None
        self.session.save()
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('sign_up')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'account/sign_up.html')

    def test_post_budget_sign_up_redirects_with_no_user_data(self):
        self.session['user_data'] = None
        self.session.save()
        response = self.client.post(self.url, follow = True)
        redirect_url = reverse('sign_up')
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'account/sign_up.html')

    def test_successful_budget_sign_up_redirects(self):
        self.session.save()
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count - 1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unsuccessful_sign_up(self):
        self.session.save()
        self.form_input['budget'] = ''
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/budget_sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SpendingLimitForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_budget_sign_up_save_user_email_as_all_lowercase(self):
        self.session['user_data']['email'] = 'JANEDOE@EXAMPLE.ORG'
        self.session.save()
        response = self.client.post(self.url, self.form_input, follow = True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        user = User.objects.get(first_name = 'Jane')
        self.assertEqual(user.email, 'janedoe@example.org')

        