from django.test import TestCase
from django.urls import reverse
from minted.models import User, FriendRequest

class FriendViewTest(TestCase):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.friend_request_id = 1
        self.form_input = {
            'email': 'janedoe@example.org',
            'is_active': 'True',
            
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
                is_active = True
            )


    def test_friend_request_url(self):
        self.assertEqual(reverse('friend_request'), '/friend_request/')
        
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
        
    def test_successful_decline(self):
        self.client.login(email=self.user.email, password="Password123")
        total_requests_before_decline = FriendRequest.objects.count()
        url = reverse('decline_request', kwargs={'friend_request_id': self.friend_request_id})
        response_url = reverse('request_list')
        response = self.client.post(url, self.form_input, follow=True)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'request_list.html')
        total_requests_after_decline = FriendRequest.objects.count()
        self.assertTrue(total_requests_after_decline == total_requests_before_decline - 1)
    



        




