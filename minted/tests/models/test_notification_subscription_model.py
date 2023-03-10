from django.test import TestCase
from django.core.exceptions import ValidationError
from minted.models import Subscription, User,NotificationSubscription

class NotificationSubscriptionModelTestCase(TestCase):
    """Unit tests for the Notification Subcription model"""

    fixtures = [
        "minted/tests/fixtures/default_user.json",
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_subscriptions.json",
        "minted/tests/fixtures/default_notification_subscriptions.json"
    ]

    def setUp(self):
        self.user = User.objects.get(email = 'johndoe@example.org')
        self.notification_subscription = NotificationSubscription.objects.get(pk=1)
    
    def test_notification_subscription_is_valid(self):
        self._assert_notification_subscription_is_valid()

    def test_notification_subscription_frequency_can_be_null(self):
        self.notification_subscription.frequency = None
        self._assert_notification_subscription_is_valid()

    def test_notification_subscription_frequency_can_be_daily(self):
        self.notification_subscription.frequency = 1
        self._assert_notification_subscription_is_valid()

    def test_notification_subscription_frequency_can_be_weekly(self):
        self.notification_subscription.frequency = 7
        self._assert_notification_subscription_is_valid()

    def test_notification_subscription_frequency_can_be_monthly(self):
        self.notification_subscription.frequency = 30
        self._assert_notification_subscription_is_valid()

    def test_notification_subscription_subscriptions_can_be_null(self):
        self.notification_subscription.subscriptions.clear()
        self._assert_notification_subscription_is_valid()

    def test_notification_subscription_subscriptions_can_all_subscriptions(self):
        count = Subscription.objects.all().count()
        subscriptions = [x for x in range(1,count+1)]
        
        self.notification_subscription.subscriptions.set(subscriptions)
        self._assert_notification_subscription_is_valid()


    def _assert_notification_subscription_is_valid(self):
        try:
            self.notification_subscription.full_clean()
        except (ValidationError):
            self.fail('Test notification_subscription should be valid')

    def _assert_notification_subscription_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.notification_subscription.full_clean()