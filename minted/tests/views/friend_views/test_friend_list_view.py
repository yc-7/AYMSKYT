from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from minted.models import User
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
        self.url = reverse('friend_list')
        self.user.friends.add(self.other_user)
    
    def _assign_friends_for_user(self, user, num_of_friends_to_add):
        all_users = list(User.objects.all().filter(is_superuser = False))
        all_users.remove(user)
        for i in range(num_of_friends_to_add):
            user.friends.add(all_users[i])

    def _create_test_users(self, user_count):
        for user_id in range(user_count):
            User.objects.create_user(
                email=f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                points = 10
            )
    

    def test_friend_list_url(self):
        self.assertEqual(self.url, '/friend_list/')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)
    
    def test_view_redirects_if_admin_user(self):
        self.client.force_login(self.other_user)
        self.assertAdminProhibited(self.url)

    def test_friend_list_contains_all_friends(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        user_friend_count = self.user.friends.all().count()
        self.assertEqual(user_friend_count, len(response.context['friends']))
        self.assertTemplateUsed(response, 'friends/friend_list.html')
    
    def test_get_friend_list_with_pagination(self):
        self.client.login(email=self.user.email, password="Password123")
        self._create_test_users(settings.FRIENDS_PER_PAGE*2-1+1)
        self._assign_friends_for_user(self.user, settings.FRIENDS_PER_PAGE*2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['friends']), settings.FRIENDS_PER_PAGE)
        self.assertTemplateUsed(response, 'friends/friend_list.html')
        self.assertTrue(response.context['is_paginated'])
        page_one_url = reverse('friend_list') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['friends']), settings.FRIENDS_PER_PAGE)
        self.assertTemplateUsed(response, 'friends/friend_list.html')
        page_two_url = reverse('friend_list') + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['friends']), settings.FRIENDS_PER_PAGE)
        self.assertTemplateUsed(response, 'friends/friend_list.html')

        