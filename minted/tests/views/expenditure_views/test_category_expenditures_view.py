from django.test import TestCase
from django.urls import reverse
from minted.models import Category, User

class CategoryExpendituresViewTestCase(TestCase):
    """Test suite for the category expenditure view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_categories.json',
        'minted/tests/fixtures/default_expenditures.json', 
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.category_name = 'Entertainment'
        self.url = reverse('category_expenditures', kwargs={'category_name':self.category_name})
        self.user = User.objects.get(pk = 1)

    def test_category_expenditures_url(self):
        self.assertEqual(self.url,f"/category_list/{self.category_name}/")

    def test_get_category_expenditures(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/expenditures_list.html')

    def test_get_category_expenditures_redirects_on_invalid_category_name(self):
        self.client.login(email = self.user.email, password = 'Password123')
        redirect_url = reverse('category_list')
        self.url = reverse('category_expenditures', kwargs={'category_name':'NOT_A_CATEGORY_NAME'})

        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_category_expenditures_shows_correct_expenditures(self):
        self.client.login(email = self.user.email, password = 'Password123')
        expenditure_count_for_user = Category.objects.filter(user = self.user, name = self.category_name).count()

        response = self.client.get(self.url)
        response_expenditure_count = response.context['expenditures'].count()
        self.assertEqual(expenditure_count_for_user, response_expenditure_count)

        for expenditure in response.context['expenditures']:
            self.assertEqual(self.category_name, expenditure.category.name)
        

