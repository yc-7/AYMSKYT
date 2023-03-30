import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from minted.models import User, Reward
from minted.forms import RewardForm
from minted.tests.helpers import LoginRequiredTester

class AddRewardsViewTestCase(TestCase, LoginRequiredTester):
    """Test suite for the add rewards view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json', 
        'minted/tests/fixtures/default_spending_limit.json',
        'minted/tests/fixtures/default_rewards.json',
    ]

    def setUp(self):
        self.reward = Reward.objects.get(pk=1)
        self.url = reverse('add_rewards')
        settings.UPLOAD_DIR = 'uploads_test/'
        self.cover_image = SimpleUploadedFile(
            "example_cover_image.png",
            b"example cover image content"
        )
        self.form_input = {
            "brand_name": "Amazon",
            "points_required": "20",
            "expiry_date": "9999-03-30",
            "description": "20% off",
            "cover_image": self.cover_image,
            "code_type": "random"}
        self.user = User.objects.get(pk = 2)
        self.other_user = User.objects.get(pk = 1)
    
    def tearDown(self):
        if os.path.exists(settings.UPLOAD_DIR):
            shutil.rmtree(settings.UPLOAD_DIR)
        
    def test_add_rewards_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'rewards/add_rewards.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RewardForm))

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)
        
    def test_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/log_in/?next=' + self.url)

    def test_view_redirects_to_dashboard_if_not_authorised(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        
    def test_add_rewards_success(self):
        self.client.force_login(self.user)
        before_count = Reward.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Reward.objects.count()
        self.assertEqual(after_count, before_count + 1)
        redirect_url = reverse('rewards_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'rewards/rewards_list.html')
        
    def test_form_invalid_data(self):
        self.client.force_login(self.user)
        self.form_input['code_type'] = 'QR'
        before_count = Reward.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Reward.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'rewards/add_rewards.html')