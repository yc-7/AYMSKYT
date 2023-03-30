from django.test import TestCase
from django.urls import reverse
from minted.models import Reward, User
from minted.tests.helpers import LoginRequiredTester

class FilteredRewardsTestCase(TestCase, LoginRequiredTester):
    """Unit tests for the Rewards Homepage view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json',
        'minted/tests/fixtures/default_rewards.json',
    ]

    def setUp(self):
        self.reward = Reward.objects.get(pk=1)
        self.url = reverse('filtered_rewards', kwargs={ 'brand_name': self.reward.brand_name })
        self.user = User.objects.get(pk=1)

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_filtered_rewards_url(self):
        self.assertEqual(self.url, f'/rewards/{self.reward.brand_name}/')

    def test_get_filtered_rewards(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rewards/rewards_home.html')

    def test_get_filtered_rewards_redirects_if_brand_does_not_exist(self):
        self.client.login(email=self.user.email, password='Password123')
        redirect_url = reverse('rewards')
        self.url = reverse('filtered_rewards', kwargs={ 'brand_name': 'x' })

        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_filtered_rewards_shows_all_rewards_with_same_brand_name(self):
        self.client.login(email=self.user.email, password='Password123')
        rewards_count = Reward.objects.filter(brand_name=self.reward.brand_name).count()
        response = self.client.get(self.url)
        response_rewards_count = response.context['rewards'].count()
        self.assertEqual(rewards_count, response_rewards_count)