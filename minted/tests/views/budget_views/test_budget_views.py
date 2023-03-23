from django.test import TestCase
from django.urls import reverse
from minted.models import User, Category, SpendingLimit, Expenditure
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from minted.tests.helpers import reverse_with_next

class BudgetListViewTestCase(TestCase):
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_third_user.json",
        "minted/tests/fixtures/default_categories.json",
        "minted/tests/fixtures/default_expenditures.json",
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.url = reverse('budget_list')
        self.user = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.category = Category.objects.get(pk=2)
        self.expenditure = Expenditure.objects.create(title = "TFL", amount = 10, date = date.today(), category = self.category)

    def test_budget_list_url(self):
        self.assertEqual(self.url, '/budget_list/')

    def test_get_budget_list_when_logged_in(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget_list.html')

    def test_get_budget_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_budget_list_shows_all_user_budgets(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget_list.html')
        end_date = date.today() - timedelta(days=date.today().weekday()) + relativedelta(days =+ 6)
        start_date = end_date - relativedelta(days =+ 6)
        amount_spent = format(self.expenditure.amount, '.2f')
        self.assertEqual(len(response.context['budget']), 3)
        self.assertContains(response, 'Overall')
        self.assertContains(response, f'£{amount_spent} out of £{self.user.budget.budget} spent')
        self.assertContains(response, str(start_date))
        self.assertContains(response, str(end_date))
        self.assertContains(response, 'Transportation')
        self.assertContains(response, f'£{amount_spent} out of £{self.category.budget.budget} spent')
        self.assertContains(response, 'Entertainment')

    def test_budget_list_does_not_show_other_user_budgets(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget_list.html')
        self.assertEqual(len(self.user.get_categories()),2)
        self.assertNotContains(response, 'Food')
        