import os
import shutil
from django.test import TestCase
from django.urls import reverse
from minted.models import User
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from minted.tests.helpers import LoginRequiredTester

class AddExpenditureViewTestCase(TestCase, LoginRequiredTester):
    """Test suite for the add expenditure view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        "minted/tests/fixtures/default_third_user.json",
        'minted/tests/fixtures/default_categories.json',
        'minted/tests/fixtures/default_expenditures.json', 
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.expenditure_id = 1
        self.category_name = 'Entertainment'
        settings.UPLOAD_DIR = 'uploads_test/'
        self.receipt = SimpleUploadedFile(
            "example_receipt.png",
            b"example receipt content"
        )
        self.form_input = {
            'title': 'expenditure1',
            'amount': 50,
            'date': datetime.date(2023, 1, 1),
            'description': '',
            'receipt': self.receipt
        }

        self.url = reverse('add_expenditure', kwargs={'category_name':self.category_name})
        self.user = User.objects.get(pk = 1)

    def tearDown(self):
        if os.path.exists(settings.UPLOAD_DIR):
            shutil.rmtree(settings.UPLOAD_DIR)
        
    def test_get_add_expenditure(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/add_expenditure.html')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_successful_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['addExpenditure'] = "Add"
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('category_expenditures', kwargs={'category_name':self.category_name})

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_expenditure_creation_with_no_file(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['receipt'] = u''
        self.form_input['addExpenditure'] = "Add"
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('category_expenditures', kwargs={'category_name':self.category_name})

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_unsuccessful_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['title'] = ''
        self.form_input['addExpenditure'] = "Add"
        
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/add_expenditure.html')

    def test_cancel_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['cancelAddition'] = "Cancel"
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('category_expenditures', kwargs={'category_name':self.category_name})

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)