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
        #print(reverse('edit_category', kwargs={'category_id': 1}))
        self.url = reverse('edit_category', kwargs={'category_id': 1})
        #print(self.url)
        self.form_input = {
            'name': 'Entertainment',
            'budget' : 160,
            'timeframe': '/month'
        }
        self.user = User.objects.get(pk = 1)


    # def test_edit_category_url(self):
    #     self.assertEqual(self.url,'/category/1/edit')
    
    # def test_successful_edit(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     print('_auth_user_id' in self.client.session.keys())
    #     category_count = len(Category.objects.all())
    #     self.form_input['name'] = 'Essentials'
    #     print(self.form_input)
    #     for cat in Category.objects.all():
    #         print(cat.name)

    #     print("adasdf")
    #     print(self.url)
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     for cat in Category.objects.all():
    #         print(cat.name)
    #     print(response.content)
    #     category_count_after = len(Category.objects.all())
    #     self.assertEqual(category_count_after, category_count)
    #     response_url = reverse('category_list')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'category_list.html')
    #     self.assertEqual(self.category.name, 'Essentials')
    #     self.assertEqual(self.category.budget, '180')