import os
import shutil
import datetime
from django.test import TestCase
from django.urls import reverse
from minted.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from minted.tests.helpers import LoginRequiredTester
from minted.forms import ExpenditureForm
from minted.models import Expenditure
from minted.tests.helpers import reverse_with_next

class AddExpenditureViewTestCase(TestCase, LoginRequiredTester):
    """Test suite for the add expenditure view."""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        "minted/tests/fixtures/default_third_user.json",
        'minted/tests/fixtures/default_categories.json',
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
            'title': 'Games',
            'amount': 50,
            'date': datetime.date(2023, 1, 1),
            'description': '',
            'receipt': self.receipt
        }

        self.url = reverse('add_expenditure', kwargs = {'category_name': self.category_name})
        self.user = User.objects.get(pk = 1)

    def tearDown(self):
        if os.path.exists(settings.UPLOAD_DIR):
            shutil.rmtree(settings.UPLOAD_DIR)

    def test_add_expenditure_url(self):
        self.assertEqual(self.url, f'/category_list/{self.category_name}/new_expenditure/')

    def test_get_add_expenditure_when_logged_in(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/add_expenditure.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ExpenditureForm))

    def test_get_add_expenditure_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)

    def test_get_add_expenditure_redirects_if_user_does_not_have_category(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.category_name = 'Food'
        self.url = reverse('add_expenditure', kwargs = {'category_name': self.category_name})
        response = self.client.get(self.url, follow = True)
        self.assertRedirects(response, '/create_category/', status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'categories/create_category.html')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_successful_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        expenditure_count_before = Expenditure.objects.count()
        self.form_input['addExpenditure'] = "Add"
        response = self.client.post(self.url, self.form_input, follow = True)
        expenditure_count_after = Expenditure.objects.count()
        self.assertEqual(expenditure_count_before, expenditure_count_after - 1)
        new_expenditure = Expenditure.objects.last()
        self.assertEqual(self.user, new_expenditure.category.user)

        redirect_url = reverse('category_expenditures', kwargs = {'category_name': self.category_name})
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code= 200)
        self.assertTemplateUsed(response, 'expenditures/expenditure_list.html')

    def test_successful_expenditure_creation_with_no_file(self):
        self.client.login(email = self.user.email, password = 'Password123')
        expenditure_count_before = Expenditure.objects.count()
        self.form_input['receipt'] = u''
        self.form_input['addExpenditure'] = "Add"
        response = self.client.post(self.url, self.form_input, follow = True)
        expenditure_count_after = Expenditure.objects.count()
        self.assertEqual(expenditure_count_before, expenditure_count_after - 1)
        new_expenditure = Expenditure.objects.last()
        self.assertEqual(self.user, new_expenditure.category.user)
        self.assertEqual(new_expenditure.receipt, u'')

        redirect_url = reverse('category_expenditures', kwargs = {'category_name': self.category_name})
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'expenditures/expenditure_list.html')
    
    def test_unsuccessful_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        expenditure_count_before = Expenditure.objects.count()
        self.form_input['title'] = ''
        self.form_input['addExpenditure'] = "Add"
        response = self.client.post(self.url, self.form_input)
        expenditure_count_after = Expenditure.objects.count()
        self.assertEqual(expenditure_count_before, expenditure_count_after)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenditures/add_expenditure.html')

    def test_cancel_expenditure_creation(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.form_input['cancelAddition'] = "Cancel"
        response = self.client.post(self.url, self.form_input, follow = True)
        redirect_url = reverse('category_expenditures', kwargs = {'category_name': self.category_name})

        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'expenditures/expenditure_list.html')

