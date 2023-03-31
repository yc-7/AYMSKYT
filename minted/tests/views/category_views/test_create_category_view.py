from django.test import TestCase
from django.urls import reverse
from minted.models import User, Category

class CreateCategoryViewTest(TestCase):
    fixtures = ['minted/tests/fixtures/default_categories.json', 
            'minted/tests/fixtures/default_spending_limit.json',
            'minted/tests/fixtures/default_user.json',
            'minted/tests/fixtures/default_other_user.json']

    def setUp(self):
        self.url = reverse('create_category')
        self.form_input = {
            'name': 'Food',
            'budget' : '160',
            'timeframe': '/month'
        }
        self.user = User.objects.get(pk = 1)


    def test_create_category_url(self):
        self.assertEqual(self.url,'/create_category/')

    def test_get_create_category(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories/create_category.html')
    
    def test_successful_creation(self):
        self.client.login(email=self.user.email, password="Password123")
        category_count_start = len(Category.objects.all())
        response = self.client.post(self.url, self.form_input, follow=True)
        category_count_end = len(Category.objects.all())
        self.assertEqual(category_count_start, category_count_end-1)
        response_url = reverse('category_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'categories/category_list.html')

    def test_unsuccessful_creation(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['budget'] = 'invalidbudget' 
        category_start_count = len(Category.objects.all())
        response = self.client.post(self.url, self.form_input, follow=True)
        category_end_count = len(Category.objects.all())
        self.assertEqual(category_start_count, category_end_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories/create_category.html')
    
    def test_unsuccessful_category_creation(self):
        self.client.login(email=self.user.email, password="Password123")
        existing_category = Category.objects.get(pk=1)
        self.form_input['name'] = existing_category.name
        category_count_start = len(Category.objects.all())
        response = self.client.post(self.url, self.form_input, follow=True)
        category_count_end = len(Category.objects.all())
        self.assertEqual(category_count_start, category_count_end)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories/create_category.html')
        form = response.context['category_form']
        self.assertEqual(form.errors['name'], ['You already have a category with this name'])
