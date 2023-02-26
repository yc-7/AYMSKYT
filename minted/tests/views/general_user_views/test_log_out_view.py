from django.test import TestCase
from django.urls import reverse
from minted.tests.helpers import LogInTester
from minted.models import User

class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the log out view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(email='johndoe@example.org')

    def test_log_out_url(self):
        self.assertEqual(self.url,'/log_out/')

    def test_get_log_out(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertFalse(self._is_logged_in())

    def test_get_log_out_without_being_logged_in(self):
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertFalse(self._is_logged_in())