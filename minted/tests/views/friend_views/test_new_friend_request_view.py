from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from minted.models import User, FriendRequest
from minted.tests.helpers import LoginRequiredTester, AdminProhibitedTester

class NewFriendViewTest(TestCase, LoginRequiredTester, AdminProhibitedTester):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_notification_subscriptions.json",
        "minted/tests/fixtures/default_subscriptions.json"
    ]

    def setUp(self):
        self.friend_request_id = 1
        self.form_input = {
            'email': 'janedoe@example.org',       
        }
        self.user = User.objects.get(pk = 1)
        self.other_user = User.objects.create (
            first_name = 'Ross',
            last_name = 'Hendricks',
            email = 'ross@example.org',
            password = 'Password123',
            points = 5
        )
        created_request = FriendRequest.objects.create(
                from_user = self.user,
                to_user = self.other_user
        )
        self.url = reverse('friend_request')
        self.admin_user = User.objects.get(pk=2)
    
    def _create_test_requests(self, request_count):
        for user_id in range(request_count):
            FriendRequest.objects.create(
                from_user =  User.objects.create_user(
                    email=f'user{user_id}@test.org',
                    password='Password123',
                    first_name=f'First{user_id}',
                    last_name=f'Last{user_id}',
                    points = 10
                ),
                to_user = self.user 
            )



    def test_friend_request_url(self):
        self.assertEqual(self.url, '/friend_request/')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_view_redirects_if_admin_user(self):
        self.client.force_login(self.admin_user)
        self.assertAdminProhibited(self.url)
        
    def test_unsuccessful_friend_request(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['email'] = 'bademail@bad.com'
        url = reverse('friend_request')
        response = self.client.post(url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friend_request.html')
        
    def test_successful_friend_request(self):
        self.client.login(email=self.user.email, password="Password123")
        url = reverse('friend_request')
        response_url = reverse('friend_request')
        response = self.client.post(url, self.form_input, follow=True)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'friend_request.html')

    def test_unsuccessful_friend_request_due_to_sent_to_self(self):
        FriendRequest.objects.all().delete()
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['email'] = self.user.email
        url = reverse('friend_request')
        response = self.client.post(url, self.form_input, follow=True)
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friend_request.html')
    
    def test_unsuccessful_friend_request_due_to_pending_friend_request_from_other_user(self):
        self.client.login(email=self.user.email, password="Password123")
        FriendRequest.objects.create(from_user = self.other_user, to_user = self.user)
        self.form_input['email'] = self.other_user.email
        url = reverse('friend_request')
        response = self.client.post(url, self.form_input, follow=True)
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friend_request.html')

    def test_unsuccessful_friend_request_due_to_pending_friend_request_to_other_user(self):
        self.client.login(email=self.user.email, password="Password123")
        FriendRequest.objects.create(from_user = self.user, to_user = self.other_user)
        self.form_input['email'] = self.other_user.email
        url = reverse('friend_request')
        response = self.client.post(url, self.form_input, follow=True)
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friend_request.html')

    def test_unsuccessful_friend_request_due_to_already_friends(self):
        self.client.login(email=self.user.email, password="Password123")
        self.user.friends.add(self.other_user)
        self.form_input['email'] = self.other_user.email
        url = reverse('friend_request')
        response = self.client.post(url, self.form_input, follow=True)
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friend_request.html')
    
    def test_get_request_list_view_with_pagination(self): 
        self.client.login(email=self.user.email, password="Password123")
        self._create_test_requests(settings.REQUESTS_PER_PAGE*2)
        response = self.client.get(reverse('request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['requests']), settings.REQUESTS_PER_PAGE)
        self.assertTemplateUsed(response, 'request_list.html')
        self.assertTrue(response.context['is_paginated'])
        page_one_url = reverse('request_list') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['requests']), settings.REQUESTS_PER_PAGE)
        self.assertTemplateUsed(response, 'request_list.html')
        page_two_url = reverse('request_list') + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['requests']), settings.REQUESTS_PER_PAGE)
        self.assertTemplateUsed(response, 'request_list.html')



        




