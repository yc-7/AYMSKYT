from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from minted.forms import EditProfileForm
from minted.models import User
from minted.tests.helpers import LoginRequiredTester

class EditProfileViewTestCase(TestCase, LoginRequiredTester):
    """Tests for the edit profile view"""
    
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]
    
    def setUp(self):
        self.url = reverse('edit_profile')
        self.user = User.objects.get(pk = 1)
        self.second_user = User.objects.get(pk = 2)
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com',
        }
        
    def test_edit_profile_url(self):
        self.assertEqual(self.url, '/profile/edit/profile/')

    def test_get_edit_profile_when_logged_in(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(form.instance, self.user)
        
    def test_get_edit_profile_when_not_logged_in(self):
        self.assertLoginRequired(self.url)
        
    def test_successful_edit_profile(self):
        self.client.login(email = self.user.email, password = 'Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'profile.html')
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 1)
        self.assertEqual(message_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe',)
        self.assertEqual(self.user.email, 'johndoe@gmail.com')
        
    def test_unsuccessful_edit_profile(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['email'] = 'INVALID_EMAIL'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
    
    def test_unsuccessful_edit_profile_due_to_duplicate_email(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['email'] = self.second_user.email
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
