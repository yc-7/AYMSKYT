from django.test import TestCase
from minted.models import User
from django.urls import reverse
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

class LoginRequiredDecoratorTestCase(TestCase):
    """Unit tests for login required decorator"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.admin_user = User.objects.get(pk=2)
        self.social_account = SocialAccount.objects.create(
            user=self.user,
            provider='google',
            uid='123456789'
        )
    
    def test_login_required_redirects_user_with_no_budget(self):
        self.user.budget = None
        self.user.save()
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(reverse('profile'), follow=True)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL), status_code=302, target_status_code=200)
    
    def test_login_required_does_not_redirect_logged_in_user(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_login_required_does_not_redirect_admin(self):
        self.client.login(email=self.admin_user.email, password='Password123')
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_login_required_does_not_redirect_admin_with_no_budget(self):
        self.admin_user.budget = None
        self.admin_user.save()
        self.client.login(email=self.admin_user.email, password='Password123')
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

