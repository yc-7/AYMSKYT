from django.test import TestCase
from minted.models import User
from django.urls import reverse
from django.conf import settings

class LogInProhibitedDecoratorTestCase(TestCase):
    """Unit tests of the prohibited decorator"""

    fixtures = [
        "minted/tests/fixtures/default_user.json",
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.admin_user = User.objects.get(pk=2)
    
    def test_login_prohibited_redirects_user_correctly(self):
        self.client.login(email = self.user.email, password = "Password123")
        response = self.client.get(reverse('log_in'), follow = True)
        self.assertRedirects(response, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER), status_code=302, target_status_code=200)

    def test_login_prohibited_redirects_admin_user_correctly(self):
        self.client.login(email = self.admin_user.email, password = "Password123")
        response = self.client.get(reverse('log_in'), follow = True)
        self.assertRedirects(response, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN), status_code=302, target_status_code=200)

    def test_staff_prohibited_redirects_admin_user_correctly(self):
        self.client.login(email=self.admin_user.email, password='Password123')
        response = self.client.get(reverse('dashboard'), follow=True)
        self.assertRedirects(response, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN), status_code=302, target_status_code=200)
    
    def test_login_prohibited_does_not_redirect_not_logged_in_user(self):
        response = self.client.get(reverse('log_in'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')