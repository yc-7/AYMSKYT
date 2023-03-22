from django.test import TestCase
from minted.models import Reward
from minted.forms import RewardForm
from datetime import date

class RewardFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            'brand_name': 'Tesco', 
            'points_required': 20, 
            'expiry_date': "2023-03-30", 
            'description': 'Food voucher', 
            'code_type': 'qr' }

    def test_form_has_necessary_fields(self):
        form = RewardForm()
        self.assertIn('brand_name', form.fields)
        self.assertIn('points_required', form.fields)
        self.assertNotIn('reward_id', form.fields)
        self.assertIn('expiry_date', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('cover_image', form.fields)
        self.assertIn('code_type', form.fields)
        self.assertIn('user_limit', form.fields)
    
    def test_valid_reward_form(self):
        form = RewardForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_reward_form(self):
        self.form_input['code_type'] = 'QR'
        form = RewardForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = RewardForm(data=self.form_input)
        before_count = Reward.objects.count()
        form.save()
        after_count = Reward.objects.count()
        self.assertEqual(after_count, before_count+1)
        reward = Reward.objects.get(brand_name = 'Tesco')
        self.assertEqual(reward.points_required, 20)
        self.assertEqual(reward.expiry_date, date(2023,3,30))
        self.assertEqual(reward.description, 'Food voucher')
        self.assertEqual(reward.code_type, 'qr')