from django.test import TestCase
from django.core.exceptions import ValidationError
from minted.models import User,Subscription

class SubscriptionModelTestCase(TestCase):
    """Unit tests for the Subcription model"""

    fixtures = [
        "minted/tests/fixtures/default_user.json",
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_subscriptions.json"
    ]

    def setUp(self):
        self.user = User.objects.get(email = 'johndoe@example.org')
        self.subscription = Subscription.objects.get(pk=1)
    
    def test_subscription_is_valid(self):
        self._assert_subscription_is_valid()

    def test_subscription_name_must_be_unique(self):
        self.subscription.name = 'Friend Requests'
        self._assert_subscription_is_invalid()

    def test_subscription_name_must_not_be_blank(self):
        self.subscription.name = ''
        self._assert_subscription_is_invalid()
    
    def test_subscription_name_may_contain_50_characters(self):
        self.subscription.name = 'x' * 50
        self._assert_subscription_is_valid()
    
    def test_subscription_name_must_not_contain_more_than_50_characters(self):
        self.subscription.name = 'x' * 51
        self._assert_subscription_is_invalid()

    def test_subscription_description_may_contain_200_characters(self):
        self.subscription.description = 'x' * 200
        self._assert_subscription_is_valid
    
    def test_subscription_description_must_not_contain_more_than_200_characters(self):
        self.subscription.description = 'x' * 201
        self._assert_subscription_is_invalid

    def test_str_function_returns_name(self):
        name = self.subscription.name
        self.assertEqual(str(self.subscription), name)

    def _assert_subscription_is_valid(self):
        try:
            self.subscription.full_clean()
        except (ValidationError):
            self.fail('Test subscription should be valid')

    def _assert_subscription_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.subscription.full_clean()