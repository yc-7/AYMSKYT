from django.test import TestCase
from django.urls import reverse
from minted.models import User, FriendRequest
from minted.tests.helpers import LoginRequiredTester

class FriendViewTest(TestCase, LoginRequiredTester):

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
        self.url = reverse('friend_list')
        self.user.friends.add(self.other_user)
    
    def test_friend_list_url(self):
        self.assertEqual(self.url, '/friend_list/')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_friend_list_contains_all_friends(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        user_friend_count = self.user.friends.all().count()
        self.assertEqual(user_friend_count, len(response.context['friends']))
        self.assertTemplateUsed(response, 'friend_list.html')