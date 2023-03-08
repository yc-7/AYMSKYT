from django.test import TestCase
from django.urls import reverse
from minted.models import User, Category, SpendingLimit
from django import forms


class DeleteCategoryViewTest(TestCase):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_categories.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('delete_category', kwargs={'category_id': 1})
        self.user = User.objects.get(pk = 1)

    def test_delete_category_url(self):
        self.assertEqual(self.url,'/category/1/delete')
    
    def test_successful_deletion(self):        
        self.client.login(email = self.user.email, password = 'Password123')
        
        category_start_count = Category.objects.all().count()
        spending_limit_start_count = SpendingLimit.objects.all().count()

        self.client.post(self.url)

        category_end_count = Category.objects.all().count()
        spending_limit_end_count = SpendingLimit.objects.all().count()

        self.assertEqual(category_start_count, category_end_count + 1)
        self.assertEqual(spending_limit_start_count, spending_limit_end_count + 1)
        
        # response_url = reverse('category_list')
        # self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        # self.assertTemplateUsed(response, 'category_list.html')
    
