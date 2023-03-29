from django.test import TestCase
from django.urls import reverse
from minted.models import User, NotificationSubscription
from minted.tests.helpers import LoginRequiredTester

class CreateNotificationSubscriptionViewTestCase(TestCase, LoginRequiredTester):
    """Test suite for the create notification subscription view."""

    fixtures = [
        "minted/tests/fixtures/default_user.json",
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_subscriptions.json",
        "minted/tests/fixtures/default_notification_subscriptions.json"
    ]

    def setUp(self):
        self.notification_subscription_id = 1
        self.form_input = {
            'frequency': 1,
            'subscriptions': [1,2]
        }

        self.url = reverse('create_notification_subscription')
        self.user = User.objects.get(pk = 1)

    def test_create_notification_subscription_url(self):
        self.assertEqual(self.url, "/notification_subscription/create")

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_get_create_notification_subscription(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notification_subscriptions/create_notification_subscription.html')

    def test_successful_notification_subscription_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('profile')

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_notification_subscription_redirects_to_edit_if_user_has_subscription(self):
        notification_subscription = NotificationSubscription.objects.get(pk=1)
        self.user.notification_subscription = notification_subscription
        self.user.save()

        self.client.login(email = self.user.email, password = 'Password123')

        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('edit_notification_subscription')

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'notification_subscriptions/edit_notification_subscription.html')
        
