import os
import shutil
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from minted.models import User, Reward
from minted.forms import RewardForm
from minted.tests.helpers import LoginRequiredTester

class EditRewardsViewTestCase(TestCase, LoginRequiredTester):
    
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        "minted/tests/fixtures/default_spending_limit.json",
        'minted/tests/fixtures/default_rewards.json',
    ]
    
    def setUp(self):
        self.reward = Reward.objects.get(pk=1)
        self.url = reverse('edit_rewards', kwargs={'reward_id':self.reward.id})
        settings.REWARDS_DIR = 'uploads_test/'
        self.cover_image = SimpleUploadedFile(
            "example_cover_image.png",
            b"example cover image content"
        )
        self.form_input = {
            "brand_name": "Apple",
            "points_required": "20",
            "expiry_date": "9999-03-30",
            "description": "20% off AirPods Max",
            "cover_image": self.cover_image,
            "code_type": "random"}
        self.user = User.objects.get(pk = 2)
        self.other_user = User.objects.get(pk = 1)

    def tearDown(self):
        if os.path.exists(settings.REWARDS_DIR):
            shutil.rmtree(settings.REWARDS_DIR)
        
    def test_edit_rewards_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'rewards/edit_rewards.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RewardForm))
        
    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_view_redirects_to_dashboard_if_not_authorised(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        
    def test_view_redirects_if_reward_does_not_exist(self):
        self.client.login(email=self.user.email, password='Password123')
        self.url = reverse('edit_rewards', kwargs={'reward_id':999})
        redirect_url = reverse('rewards_list')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_edit_rewards_success(self):
        self.client.force_login(self.user)
        self.form_input['points_required'] = '50'
        self.form_input['code_type'] = 'qr'
        before_count = Reward.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Reward.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('rewards_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'rewards/rewards_list.html')
        self.reward.refresh_from_db()
        self.assertEqual(self.reward.points_required, 50)
        self.assertEqual(self.reward.code_type, 'qr')

    def test_form_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'code_type': 'QR'})
        self.assertTemplateUsed(response, 'rewards/edit_rewards.html')