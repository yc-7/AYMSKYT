from django.test import TestCase
from minted.forms import EditProfileForm
from django import forms


class EditProfileFormTest(TestCase):
    
    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        
    def test_valid_form_data(self):
        form = EditProfileForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_form_has_fields(self):
        form = EditProfileForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertEqual(isinstance(email_field, forms.EmailField), True)
    
    def test_blank_data(self):
        form = EditProfileForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.'],
        })
        
    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'bademail'
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_rejects_empty_email(self):
        self.form_input['email'] = ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    
        
    