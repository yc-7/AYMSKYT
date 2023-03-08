from django.test import TestCase
from django.urls import reverse
from minted.models import User, Category
from django import forms


class DeleteCategoryViewTest(TestCase):
    fixtures = ['minted/tests/fixtures/default_categories.json', 
            'minted/tests/fixtures/default_spending_limit.json',
            'minted/tests/fixtures/default_user.json',
            'minted/tests/fixtures/default_other_user.json']

    def setUp(self):
        self.url = reverse('delete_category', kwargs={'category_id': 1})
        self.user = User.objects.get(pk = 1)


    def test_delete_category_url(self):
        self.assertEqual(self.url,'/category/1/delete')
    
    # def test_successful_deletion(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     category_count = len(Category.objects.all())
    #     self.client.post(self.url)
    #     end_category_count = len(Category.objects.all())
    #     self.assertEqual(category_count, end_category_count+1)
        # for cat in Category.objects.all():
        #     print(cat.budget)
        
        # response_url = reverse('category_list')
        # self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        # self.assertTemplateUsed(response, 'category_list.html')
    
