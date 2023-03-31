from django.test import TestCase
from django.urls import reverse
from minted.models import User
from minted.tests.helpers import LoginRequiredTester


class EditSpendingLimitViewTestCase(TestCase, LoginRequiredTester):
    
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]
    
    def setUp(self):
        self.url = reverse('edit_spending_limit')
        self.form_input = {
            'budget': '200',
            'timeframe': '/month'
        }
        self.user = User.objects.get(pk = 1)
        
    
    def test_edit_spending_limit_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'edit_spending_limit.html')
        
    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)
           
    def test_spending_limit_successfully_changes(self):
        self.client.force_login(self.user)
        self.assertEqual(self.user.budget.budget, 150.00)
        self.assertEqual(self.user.budget.timeframe, '/week')
        response = self.client.post(self.url, data=self.form_input)
        self.assertRedirects(response, '/profile/', status_code=302, target_status_code=200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.budget.budget, 200.00)
        self.assertEqual(self.user.budget.timeframe, '/month')
        
    def test_form_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'budget': 100.1})
        self.assertTemplateUsed(response, 'edit_spending_limit.html')
        self.assertEqual(self.user.budget.budget, 150.00)
        self.assertEqual(self.user.budget.timeframe, '/week')