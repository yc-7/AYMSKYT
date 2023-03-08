from django.test import TestCase
from django.urls import reverse
from minted.models import User, Category
from django import forms


class CreateCategoryViewTest(TestCase):
    fixtures = ['minted/tests/fixtures/default_categories.json', 
            'minted/tests/fixtures/default_spending_limit.json',
            'minted/tests/fixtures/default_user.json',
            'minted/tests/fixtures/default_other_user.json']

    def setUp(self):
        self.url = reverse('create_category')
        self.form_input = {
            'name': 'Entertainment',
            'budget' : '160',
            'timeframe': '/month'
        }
        self.user = User.objects.get(pk = 1)


    def test_get_create_category_url(self):
        self.assertEqual(self.url,'/create_category/')
    
    def test_successful_creation(self):
        self.client.login(email=self.user.email, password="Password123")
        category_count = len(Category.objects.all())
        self.assertEqual(category_count, 3)
        response = self.client.post(self.url, self.form_input, follow=True)
        category_count = len(Category.objects.all())
        self.assertEqual(category_count, 4)
        response_url = reverse('category_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'category_list.html')
    
