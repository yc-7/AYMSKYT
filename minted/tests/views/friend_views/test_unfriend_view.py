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
        self.user.friends.add(self.other_user)
        self.friend_id = self.other_user.id
        self.url = reverse('unfriend', kwargs={'friend_id': self.friend_id})
    
    def test_unfriend_url(self):
        self.assertEqual(self.url, f'/unfriend/{self.friend_id}')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)
    
    def test_view_redirects_if_admin_user(self):
        self.client.force_login(self.other_user)
        self.assertAdminProhibited(self.url)

    def test_successful_unfriend(self):
        self.client.login(email = self.user.email, password = 'Password123')
        friend_count_start_count = self.user.friends.all().count()
        response = self.client.post(self.url, follow=True)
        friend_count_end_count = self.user.friends.all().count()
        self.assertEqual(friend_count_start_count, friend_count_end_count+1)
        self.assertTemplateUsed(response, 'friends/friend_list.html')
        redirect_url = reverse('friend_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_unfriend_request_redirects(self):
        self.client.login(email = self.user.email, password = 'Password123')
        friend_start_count = self.user.friends.all().count()
        response = self.client.get(self.url, follow=True)
        friend_end_count = self.user.friends.all().count()
        self.assertEqual(friend_start_count, friend_end_count)
        self.assertTemplateUsed(response, 'friends/friend_list.html')
        redirect_url = reverse('friend_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_unfriend_view_redirects_if_friend_id_of_user_that_is_not_a_friend_provided(self):
        self.url = reverse('unfriend', kwargs={'friend_id': 100})
        self.client.login(email = self.user.email, password = 'Password123')
        friend_start_count = self.user.friends.all().count()
        response = self.client.post(self.url, follow=True)
        friend_end_count = self.user.friends.all().count()
        self.assertEqual(friend_start_count, friend_end_count)
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(response.status_code, 404)