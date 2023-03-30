from django import forms
from django.test import TestCase
from minted.forms import EditProfileForm
from minted.models import User

class EditProfileFormTest(TestCase):
    """Unit tests for the user form"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(pk = 1)
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com'
        }

    def test_form_contains_required_fields(self):
        form = EditProfileForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        
    def test_form_accepts_valid_input(self):
        form = EditProfileForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_first_name(self):
        self.form_input['first_name'] = ''
        form = EditProfileForm(data = self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_last_name(self):
        self.form_input['last_name'] = ''
        form = EditProfileForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = EditProfileForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'INVALID_EMAIL'
        form = EditProfileForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_correctly(self):
        form = EditProfileForm(instance = self.user, data = self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@gmail.com')

    def test_form_saves_email_as_all_lowercase(self):
        self.form_input['email'] = 'JOHNDOE@GMAIL.COM'
        form = EditProfileForm(instance = self.user, data = self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@gmail.com')
        
    