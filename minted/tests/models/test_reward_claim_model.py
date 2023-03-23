from django.core.exceptions import ValidationError
from django.test import TestCase
from minted.models import RewardClaim

class RewardClaimTestCase(TestCase):
    """Unit tests for the RewardClaim model"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json',
        'minted/tests/fixtures/default_rewards.json',
        'minted/tests/fixtures/default_reward_claims.json'
    ]

    def setUp(self):
        self.claim = RewardClaim.objects.get(pk=1)
        self.second_claim = RewardClaim.objects.get(pk=2)

    def test_claim_code_contains_10_chars(self):
        self.claim.claim_code = 'x' * 10
        self._assert_reward_claim_is_valid()

    def test_claim_code_cannot_contain_more_than_10_chars(self):
        self.claim.claim_code = 'x' * 11
        self._assert_reward_claim_is_invalid()

    def test_claim_code_can_be_blank(self):
        self.claim.claim_code = ''
        self._assert_reward_claim_is_valid()

    def test_claim_code_must_be_unique(self):
        self.claim.claim_code = self.second_claim.claim_code
        self._assert_reward_claim_is_invalid()

    def test_claim_qr_can_be_blank(self):
        self.claim.claim_qr = None
        self._assert_reward_claim_is_valid()

    def _assert_reward_claim_is_valid(self):
        try:
            self.claim.full_clean()
        except ValidationError:
            self.fail("Test claim should be valid")

    def _assert_reward_claim_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.claim.full_clean()
