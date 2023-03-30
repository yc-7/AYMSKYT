from django.test import TestCase
from django.urls import reverse
from minted.models import RewardClaim, User
from minted.tests.helpers import LoginRequiredTester

class MyRewardsViewTestCase(TestCase, LoginRequiredTester):
    """Unit tests for the My Rewards view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json',
        'minted/tests/fixtures/default_rewards.json',
        'minted/tests/fixtures/default_reward_claims.json'
    ]

    def setUp(self):
        self.url = reverse('my_rewards')
        self.user = User.objects.get(pk=1)
    
    def test_my_rewards_url(self):
        self.assertEqual(self.url, '/rewards/my_rewards/')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_get_my_rewards(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rewards/my_rewards.html')

    def test_get_my_rewards_shows_all_user_claims(self):
        self.client.login(email=self.user.email, password='Password123')
        claims_count = RewardClaim.objects.filter(user=self.user).count()
        response = self.client.get(self.url)
        response_claims_count = response.context['claimed_rewards'].count()
        self.assertEqual(claims_count, response_claims_count)
        