from django.test import TestCase
from django.urls import reverse
from minted.models import Reward, User
from minted.tests.helpers import LoginRequiredTester

class RewardListViewTestCase(TestCase, LoginRequiredTester):
    """Unit tests for the Rewards List view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json',
        'minted/tests/fixtures/default_rewards.json'
    ]

    def setUp(self):
        self.url = reverse('rewards_list')
        self.user = User.objects.get(pk=2)
        self.other_user = User.objects.get(pk=1)
    
    def test_rewards_list_url(self):
        self.assertEqual(self.url, '/rewards/admin')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_get_rewards_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rewards/rewards_list.html')

    def test_get_rewards_list_for_unauthorised_user(self):
        self.client.login(email=self.other_user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_rewards_list_shows_all_rewards(self):
        self.client.login(email=self.user.email, password='Password123')
        rewards_count = Reward.objects.all().count()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['rewards']), rewards_count)