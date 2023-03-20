from django.core.exceptions import ValidationError
from django.test import TestCase
from minted.models import Reward

class RewardModelTestCase(TestCase):
    """Unit tests for the Reward model"""

    fixtures = [
        'minted/tests/fixtures/default_rewards.json'
    ]

    def setUp(self):
        self.reward = Reward.objects.get(pk=1)
        self.other_reward = Reward.objects.get(pk=3)

    def test_reward_is_valid(self):
        self._assert_reward_is_valid()

    def test_brand_name_contains_50_chars(self):
        self.reward.brand_name = 'x' * 50
        self._assert_reward_is_valid()
    
    def test_brand_name_cannot_contain_more_than_50_chars(self):
        self.reward.brand_name = 'x' * 51
        self._assert_reward_is_invalid()

    def test_brand_name_cannot_be_blank(self):
        self.reward.brand_name = ''
        self._assert_reward_is_invalid()

    def test_points_required_can_be_1(self):
        self.reward.points_required = 1
        self._assert_reward_is_valid()
    
    def test_points_required_cannot_be_less_than_1(self):
        self.reward.points_required = 0
        self._assert_reward_is_invalid()
 
    def test_points_required_cannot_be_blank(self):
        self.reward.points_required = None
        self._assert_reward_is_invalid()

    def test_reward_id_contains_6_chars(self):
        self.reward.reward_id = 'x' * 6
        self._assert_reward_is_valid()

    def test_reward_id_cannot_contain_more_than_6_chars(self):
        self.reward.reward_id = 'x' * 7
        self._assert_reward_is_invalid()

    def test_reward_id_must_be_unique(self):
        self.reward.reward_id = self.other_reward.reward_id
        self._assert_reward_is_invalid()

    def test_reward_id_cannot_be_blank(self):
        self.reward.reward_id = ''
        self._assert_reward_is_invalid()
 
    def test_expiry_date_cannot_be_blank(self):
        self.reward.expiry_date = None
        self._assert_reward_is_invalid()
 
    def test_description_can_contain_300_chars(self):
        self.reward.description = 'x' * 300
        self._assert_reward_is_valid()

    def test_description_cannot_contain_more_than_300_chars(self):
        self.reward.description = 'x' * 301
        self._assert_reward_is_valid()

    def test_description_cannot_be_blank(self):
        self.reward.description = ''
        self._assert_reward_is_invalid()

    def test_cover_image_can_be_blank(self):
        self.reward.cover_image = None
        self._assert_reward_is_valid()

    def test_code_type_can_be_qr_code(self):
        self.reward.code_type = 'qr'
        self._assert_reward_is_valid()

    def test_code_type_can_be_random_code(self):
        self.reward.code_type = 'random'
        self._assert_reward_is_valid()

    def test_code_type_cannot_be_anything_but_qr_or_random(self):
        self.reward.code_type = 'x'
        self._assert_reward_is_invalid()

    def _assert_reward_is_valid(self):
        try:
            self.reward.full_clean()
        except ValidationError:
            self.fail("Test reward should be valid")

    def _assert_reward_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.reward.full_clean()



    