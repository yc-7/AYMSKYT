import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
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
        self.reward = Reward.objects.get(pk=1)
        settings.UPLOAD_DIR = 'uploads_test/'
        self.cover_image = SimpleUploadedFile(
            "example_cover_image.png",
            b"example cover image content"
        )
    
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

    def test_delete_reward(self):
        self.client.login(email = self.user.email, password='Password123')
        rewards_before = Reward.objects.count()
        self.reward.cover_image = self.cover_image
        self.reward.save()
        remove = {'delete': '1'}
        response = self.client.post(self.url, remove, follow = True)
        rewards_after = Reward.objects.count()
        response_url = reverse('rewards_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'rewards/rewards_list.html')
        self.assertEqual(rewards_before, rewards_after+1)