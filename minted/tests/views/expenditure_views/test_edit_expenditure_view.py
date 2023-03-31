import filecmp
from django.test import TestCase
from django.urls import reverse
from minted.models import Expenditure, User
import datetime
from django.conf import settings
import os
import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from minted.tests.helpers import LoginRequiredTester

class ExpenditureEditViewTestCase(TestCase, LoginRequiredTester):
    """Test suite for the expenditure edit view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_third_user.json',
        'minted/tests/fixtures/default_categories.json',
        'minted/tests/fixtures/default_expenditures.json', 
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        settings.UPLOAD_DIR = 'uploads_test/'
        self.expenditure_id = 1
        self.category_name = 'Entertainment'
        self.form_input = {
            'title': 'expenditure1',
            'amount': 50,
            'date': datetime.date(2023, 1, 1),
            'description': ''
        }

        self.url = reverse('edit_expenditure', kwargs={'category_name':self.category_name, 'expenditure_id':self.expenditure_id})
        self.user = User.objects.get(pk = 1)

        # Create expenditure receipt
        if not os.path.exists(settings.UPLOAD_DIR):
            os.mkdir(settings.UPLOAD_DIR)
        self.new_reciept_path = os.path.join(settings.UPLOAD_DIR, 'test_receipt.png')
        with open(self.new_reciept_path, 'w') as f:
            f.write("reciept_test_content")
        expenditure = Expenditure.objects.get(pk=self.expenditure_id)
        expenditure.receipt = self.new_reciept_path
        expenditure.save()

    def tearDown(self):
        if os.path.exists(settings.UPLOAD_DIR):
            shutil.rmtree(settings.UPLOAD_DIR)
        
    def test_edit_expenditure_url(self):
        self.assertEqual(self.url,f"/category_list/{self.category_name}/edit_expenditure/{self.expenditure_id}/")

    def test_get_edit_expenditure(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/edit_expenditures.html')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_successful_expenditure_edit(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('category_expenditures', kwargs={'category_name':self.category_name})

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

        expenditure = response.context['expenditures'][0]
        self.assertEqual(expenditure.title, self.form_input['title'])
        self.assertEqual(expenditure.amount, self.form_input['amount'])
        self.assertEqual(expenditure.date, self.form_input['date'])
        self.assertEqual(expenditure.description, self.form_input['description'])
        self.assertEqual(expenditure.receipt, self.new_reciept_path)

    def test_successful_expenditure_edit_with_file(self):
        self.client.login(email = self.user.email, password = 'Password123')
        new_file = SimpleUploadedFile(
            "example_receipt.png",
            b"example receipt content"
        )
        self.form_input['receipt'] = new_file
        num_files_in_folder_start_count = len([f for f in os.listdir(settings.UPLOAD_DIR)])

        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('category_expenditures', kwargs={'category_name':self.category_name})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        expenditure = response.context['expenditures'][0]
        self.assertEqual(expenditure.title, self.form_input['title'])
        self.assertEqual(expenditure.amount, self.form_input['amount'])
        self.assertEqual(expenditure.date, self.form_input['date'])
        self.assertEqual(expenditure.description, self.form_input['description'])

        num_files_in_folder_end_count = len([f for f in os.listdir(settings.UPLOAD_DIR)])

        self.assertEqual(num_files_in_folder_start_count, num_files_in_folder_end_count)

    def test_unsuccessful_expenditure_edit_rerenders_page(self):
        self.client.login(email = self.user.email, password = 'Password123')
        expenditure = Expenditure.objects.get(pk=self.expenditure_id)
        self.form_input['title'] = ''

        response = self.client.post(self.url, self.form_input)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)

    def test_redirect_on_invalid_expenditure_id(self):
        self.client.login(email = self.user.email, password = 'Password123')
        expenditure_id_that_does_not_exist = 100
        self.url = reverse('edit_expenditure', kwargs={'category_name':self.category_name, 'expenditure_id':expenditure_id_that_does_not_exist})

        redirect_url = reverse('category_list')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_redirect_on_edit_another_users_expenditure(self):
        self.client.login(email = self.user.email, password = 'Password123')
        expenditure_id_that_belongs_to_other_user = 3
        self.url = reverse('edit_expenditure', kwargs={'category_name':self.category_name, 'expenditure_id':expenditure_id_that_belongs_to_other_user})

        redirect_url = reverse('category_list')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
