from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from minted.models import User
from minted.forms import SignUpForm

class SignUpViewTestCase(TestCase):
    """Tests of the sign up view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.user = User.objects.get(pk=1)


    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_sign_up_stores_user_session_data(self):
        response = self.client.post(self.url, {**self.form_input})
        user_data = response.client.session.get('user_data')
        self.assertEqual(user_data['first_name'], self.form_input['first_name'])
        self.assertEqual(user_data['last_name'], self.form_input['last_name'])
        self.assertEqual(user_data['email'], self.form_input['email'])
        self.assertEqual(user_data['new_password'], self.form_input['new_password'])
        self.assertEqual(user_data['password_confirmation'], self.form_input['password_confirmation'])

    def test_sign_up_redirects(self):
        response = self.client.post(self.url, {**self.form_input}, follow=True)
        response_url = reverse('spending_signup')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'account/spending_signup.html')
