from django.test import TestCase
from django.urls import reverse
from minted.models import Reward, User
from minted.tests.helpers import LoginRequiredTester

class RewardHomepageViewTestCase(TestCase, LoginRequiredTester):
    """Unit tests for the Rewards Homepage view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json',
        'minted/tests/fixtures/default_rewards.json'
    ]

    def setUp(self):
        self.url = reverse('rewards')
        self.user = User.objects.get(pk=1)
    
    def test_rewards_homepage_url(self):
        self.assertEqual(self.url, '/rewards/')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_get_rewards_homepage(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rewards/rewards_home.html')

    def test_get_rewards_homepage_shows_all_rewards(self):
        self.client.login(email=self.user.email, password='Password123')
        rewards_count = Reward.objects.all().count()
        response = self.client.get(self.url)
        response_rewards_count = response.context['rewards'].count()
        self.assertEqual(rewards_count, response_rewards_count)

