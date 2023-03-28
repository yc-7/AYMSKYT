from django.test import TestCase
from django.urls import reverse
from minted.models import User
from django.contrib import messages


class EditProfileViewTestCase(TestCase):
    
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]
    
    def setUp(self):
        self.url = reverse('edit_profile')
        self.form_input = {
            'first_name': 'TestName',
            'last_name': 'TestLastname',
            'email': 'test@example.org',
        }
        self.user = User.objects.get(pk = 1)
        
    def test_edit_profile_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'edit_profile.html')
        
    def test_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/log_in/?next=' + self.url)
        
    def test_original_data(self):
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
        
    def test_edit_profile_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.form_input)
        self.assertRedirects(response, '/profile/', status_code=302, target_status_code=200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'TestName')
        self.assertEqual(self.user.last_name, 'TestLastname',)
        self.assertEqual(self.user.email, 'test@example.org')
        
    def test_form_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'email': 'invalid'})
        self.assertTemplateUsed(response, 'edit_profile.html')
    
