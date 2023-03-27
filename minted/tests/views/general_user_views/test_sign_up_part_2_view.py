from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from minted.models import User
from minted.forms import SignUpForm2, SpendingLimitForm

class SignUpPart2ViewTestCase(TestCase):
    """Tests of the sign up view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('sign_up_part2')
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.user = User.objects.get(pk=1)

    def test_sign_up_part_2_url(self):
        self.assertEqual(self.url, '/sign_up/account_details/')

    def test_get_sign_up_part_2(self):
        session = self.client.session
        session['user_email'] = 'janedoe@example.org'
        session.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        form = response.context['form']
        part = response.context['part']
        self.assertTrue(isinstance(form, SignUpForm2))
        self.assertEqual(part, 2)
        self.assertFalse(form.is_bound)

    def test_get_sign_up_part_2_redirects_with_no_email_data(self):
        session = self.client.session
        session['user_email'] = None
        session.save()
        response = self.client.get(self.url)
        redirect_url = reverse('sign_up')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_get_sign_up_part_2_redirects_with_valid_data(self):
        session = self.client.session
        session['user_email'] = 'janedoe@example.org'
        session.save()
        response = self.client.post(self.url, {**self.form_input}, follow = True)
        response_url = reverse('spending_signup')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'account/spending_signup.html')