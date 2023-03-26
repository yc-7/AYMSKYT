from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from minted.models import User, SpendingLimit
from minted.forms import SignUpForm1, SpendingLimitForm

class SignUpPart1ViewTestCase(TestCase):
    """Tests of the sign up view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'email': 'janedoe@example.org',
        }
        self.user = User.objects.get(pk=1)

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        form = response.context['form']
        part = response.context['part']
        self.assertTrue(isinstance(form, SignUpForm1))
        self.assertEqual(part, 1)
        self.assertFalse(form.is_bound)

    def test_get_sign_up_redirects_valid_email(self):
        response = self.client.post(self.url, {**self.form_input}, follow = True)
        redirect_url = reverse('sign_up_part2')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'account/signup.html')

