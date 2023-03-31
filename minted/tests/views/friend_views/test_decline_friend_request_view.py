from django.test import TestCase
from django.urls import reverse
from minted.models import User, FriendRequest
from minted.tests.helpers import LoginRequiredTester, AdminProhibitedTester

class FriendRequestDeclineViewTest(TestCase, LoginRequiredTester, AdminProhibitedTester):

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
        self.friend_request = FriendRequest.objects.create(
            from_user = self.other_user,
            to_user = self.user,
        )
        self.url = reverse('decline_request', kwargs={'friend_request_id': self.friend_request.id})
    
    def test_friend_list_url(self):
        self.assertEqual(self.url, f'/decline_request/{self.friend_request.id}')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_view_redirects_if_admin_user(self):
        self.client.force_login(self.other_user)
        self.assertAdminProhibited(self.url)

    def test_get_decline_friend_request_redirects(self):
        self.client.login(email = self.user.email, password = 'Password123')
        friend_request_start_count = FriendRequest.objects.count()
        response = self.client.get(self.url, follow=True)
        friend_request_end_count = FriendRequest.objects.count()
        self.assertEqual(friend_request_start_count, friend_request_end_count)
        self.assertTemplateUsed(response, 'friends/request_list.html')
        redirect_url = reverse('request_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_successful_decline(self):
        self.client.login(email=self.user.email, password="Password123")
        total_requests_before_decline = FriendRequest.objects.count()
        response_url = reverse('request_list')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'friends/request_list.html')
        total_requests_after_decline = FriendRequest.objects.count()
        self.assertTrue(total_requests_before_decline, total_requests_after_decline+1)

    def test_post_decline_friend_request_view_redirects_if_invalid_friend_request_id_provided(self):
        self.url = reverse('decline_request', kwargs={'friend_request_id': 100})
        self.client.login(email = self.user.email, password = 'Password123')
        friend_request_start_count = FriendRequest.objects.count()
        response = self.client.post(self.url, follow=True)
        friend_request_end_count = FriendRequest.objects.count()
        self.assertEqual(friend_request_start_count, friend_request_end_count)
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(response.status_code, 404)