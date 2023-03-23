from django.test import TestCase
from django.urls import reverse
from minted.models import User, Category
from django import forms
from minted.forms import CategoryForm


class EditExpenditureViewTestCase(TestCase):
    fixtures = ['minted/tests/fixtures/default_categories.json', 
            'minted/tests/fixtures/default_spending_limit.json',
            'minted/tests/fixtures/default_user.json',
            'minted/tests/fixtures/default_other_user.json']

    def setUp(self):
        self.category_id = 1
        self.url = reverse('edit_category', kwargs={'category_id': self.category_id})
        self.form_input = {
            'name': 'Entertainment',
            'budget' : 160,
            'timeframe': '/month',
        }
        self.user = User.objects.get(pk = 1)


    def test_edit_category_url(self):
        self.assertEqual(self.url,f'/category/{self.category_id}/edit')

    def test_get_edit_category(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_category.html')

    def test_edit_category_redirects_if_category_does_not_exist(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.url = reverse('edit_category', kwargs={'category_id': 100})
        response = self.client.get(self.url, follow=True)
        response_url = reverse('create_category')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'create_category.html')
    
    # def test_successful_edit(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     category_count = len(Category.objects.all())
    #     self.form_input['name'] = 'Essentials'
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     form = CategoryForm(data = self.form_input)
    #     category_count_after = len(Category.objects.all())
    #     self.assertEqual(category_count_after, category_count)
    #     response_url = reverse('category_list')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'category_list.html')
    #     self.assertEqual(form['name'].value(),'Essentials')