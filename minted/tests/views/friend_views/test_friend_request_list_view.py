from django.test import TestCase
from django.urls import reverse
from minted.models import User, FriendRequest
from minted.tests.helpers import LoginRequiredTester, AdminProhibitedTester

class FriendViewTest(TestCase, LoginRequiredTester, AdminProhibitedTester):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_notification_subscriptions.json",
        "minted/tests/fixtures/default_subscriptions.json"
    ]

    def setUp(self):
        self.friend_request_id = 1
        self.user = User.objects.get(pk = 1)
        self.other_user = User.objects.get(pk = 2)
        FriendRequest.objects.create(
            from_user = self.other_user,
            to_user = self.user,
        )
        self.url = reverse('request_list')
    
    def test_friend_list_url(self):
        self.assertEqual(self.url, '/request_list/')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)
    
    def test_view_redirects_if_admin_user(self):
        self.client.force_login(self.other_user)
        self.assertAdminProhibited(self.url)

    def test_friend_request_list_contains_all_friend_requests(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        friend_requests_sent_to_current_user = FriendRequest.objects.filter(to_user = self.user).count()
        self.assertEqual(friend_requests_sent_to_current_user, len(response.context['requests']))
        self.assertTemplateUsed(response, 'request_list.html')