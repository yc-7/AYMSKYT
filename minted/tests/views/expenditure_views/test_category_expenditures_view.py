from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from minted.models import Category, User, Expenditure
from minted.tests.helpers import LoginRequiredTester

class CategoryExpendituresViewTestCase(TestCase, LoginRequiredTester):
    """Test suite for the category expenditure view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        "minted/tests/fixtures/default_third_user.json",
        'minted/tests/fixtures/default_categories.json',
        'minted/tests/fixtures/default_expenditures.json', 
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.category_name = 'Entertainment'
        self.url = reverse('category_expenditures', kwargs={'category_name':self.category_name})
        self.user = User.objects.get(pk = 1)
        self.category = Category.objects.get(pk=1)

    def _create_test_expenditures(self, expenditure_count):
        for user_id in range(expenditure_count):
            Expenditure.objects.create(
                category =  self.category,
                title = 'Entertainment',
                amount = 30,
                date = "2023-01-26",

            )

    def test_category_expenditures_url(self):
        self.assertEqual(self.url,f"/category_list/{self.category_name}/")

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_get_category_expenditures(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/expenditure_list.html')

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

    def test_get_category_expenditures_list_with_pagination(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self._create_test_expenditures(settings.EXPENDITURES_PER_PAGE*2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['expenditures']), settings.EXPENDITURES_PER_PAGE)
        self.assertTemplateUsed(response, 'expenditures/expenditure_list.html')
        self.assertTrue(response.context['is_paginated'])
        page_one_url = reverse('category_expenditures', kwargs={'category_name': self.category.name}) + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['expenditures']), settings.EXPENDITURES_PER_PAGE)
        self.assertTemplateUsed(response, 'expenditures/expenditure_list.html')
        page_two_url = reverse('category_expenditures', kwargs={'category_name': self.category.name}) + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['expenditures']), settings.EXPENDITURES_PER_PAGE)
        self.assertTemplateUsed(response, 'expenditures/expenditure_list.html')

