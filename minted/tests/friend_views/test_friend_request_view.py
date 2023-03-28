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
        self.form_input = {
            'email': 'janedoe@example.org',       
        }
        self.user = User.objects.get(pk = 1)
        self.other_user = User.objects.create (
            first_name = 'Ross',
            last_name = 'Hendricks',
            email = 'ross@example.org',
            points = 5
        )
        created_request = FriendRequest.objects.create(
                from_user = self.user,
                to_user = self.other_user,
        )
        self.url = reverse('friend_request')


    def test_friend_request_url(self):
        self.assertEqual(self.url, '/friend_request/')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)
        
    def test_unsuccessful_friend_request(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['email'] = 'bademail@bad.com'
        url = reverse('friend_request')
        response_url = reverse('friend_request')
        response = self.client.post(url, self.form_input, follow=True)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'friend_request.html')
        
    def test_successful_friend_request(self):
        self.client.login(email=self.user.email, password="Password123")
        url = reverse('friend_request')
        response_url = reverse('profile')
        response = self.client.post(url, self.form_input, follow=True)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
    



        




