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
        self.friend_request_id = 1
        self.url = reverse('accept_request', kwargs={'friend_request_id': self.friend_request_id})

    def test_friend_list_url(self):
        self.assertEqual(self.url, f'/accept_request/{self.friend_request_id}')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)
    
    def test_view_redirects_if_admin_user(self):
        self.client.force_login(self.other_user)
        self.assertAdminProhibited(self.url)

    def test_successful_accept(self):
        self.client.login(email=self.user.email, password="Password123")
        total_requests_before_accept = FriendRequest.objects.count()
        senders_total_friends_before_accept = self.user.friends.count()
        recipients_total_friends_before_accept = self.other_user.friends.count()
        response_url = reverse('request_list')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'friends/request_list.html')
        total_requests_after_accept = FriendRequest.objects.count()
        senders_total_friends_after_accept = self.user.friends.count()
        recipients_total_friends_after_accept = self.other_user.friends.count()
        self.assertTrue(total_requests_after_accept == total_requests_before_accept - 1)
        self.assertTrue(senders_total_friends_after_accept == senders_total_friends_before_accept + 1)
        self.assertTrue(recipients_total_friends_after_accept == recipients_total_friends_before_accept + 1)

    def test_redirects_if_user_has_no_friend_requests(self):
        self.client.login(email=self.user.email, password="Password123")
        for request in FriendRequest.objects.all():
            request.delete()

        response_url = reverse('request_list')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_get_accept_friend_request_redirects(self):
        self.client.login(email = self.user.email, password = 'Password123')
        friend_request_start_count = FriendRequest.objects.count()
        response = self.client.get(self.url, follow=True)
        friend_request_end_count = FriendRequest.objects.count()
        self.assertEqual(friend_request_start_count, friend_request_end_count)
        self.assertTemplateUsed(response, 'friends/request_list.html')
        redirect_url = reverse('request_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        