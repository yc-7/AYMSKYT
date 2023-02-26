from django.test import TestCase
from django.core.exceptions import ValidationError
from minted.models import SpendingLimit

class SpendingLimitModelTestCase(TestCase):
    """Unit tests for the Spending Limit model"""

    fixtures = [
        "minted/tests/fixtures/default_spending_limit.json",
    ]

    def setUp(self):
        self.limit = SpendingLimit.objects.get(pk = 1)

    def test_budget_must_not_be_longer_than_12_digits(self):
        self.limit.budget = 12345678901.00
        self._assert_spending_is_invalid()

    def test_budget_can_be_12_digits(self):
        self.limit.budget = 1234567890.00
        self._assert_spending_is_valid()
    
    def test_budget_cannot_be_blank(self):
        self.limit.budget = None
        self._assert_spending_is_invalid()
    
    def test_budget_must_be_2_decimal_places(self):
        self.limit.budget = 123.1
        self._assert_spending_is_invalid()
    
    def test_timeframe_cannot_be_blank(self):
        self.limit.timeframe = None
        self._assert_spending_is_invalid()

    def _assert_spending_is_valid(self):
        try:
            self.limit.full_clean()
        except (ValidationError):
            self.fail('Test should be valid')

    def _assert_spending_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.limit.full_clean()