from django.test import TestCase
from django.urls import reverse
from minted.models import Category, Expenditure, User
import datetime

class AddExpenditureViewTestCase(TestCase):
    """Test suite for the add expenditure view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_categories.json',
        'minted/tests/fixtures/default_expenditures.json', 
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.expenditure_id = 1
        self.category_name = 'Entertainment'
        self.form_input = {
            'title': 'expenditure1',
            'amount': 50,
            'date': datetime.date(2023, 1, 1),
            'description': ''
        }

        self.url = reverse('add_expenditure', kwargs={'category_name':self.category_name})
        self.user = User.objects.get(pk = 1)

    def test_get_add_expenditure(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/add_expenditure.html')

    def test_successful_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['addExpenditure'] = "Add"
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('category_expenditures', kwargs={'category_name':self.category_name})

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cancel_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['cancelAddition'] = "Cancel"
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('category_expenditures', kwargs={'category_name':self.category_name})

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)