from django.test import TestCase
from django.urls import reverse
from minted.models import User, Category, Expenditure
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from minted.tests.helpers import LoginRequiredTester

class BudgetListViewTestCase(TestCase, LoginRequiredTester):
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_other_user.json",
        "minted/tests/fixtures/default_third_user.json",
        "minted/tests/fixtures/default_categories.json",
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.url = reverse('budget_list')
        self.today = date.today()
        self.user = User.objects.get(pk=1)
        self.other_category = Category.objects.get(pk=2)
        self.category = Category.objects.get(pk=1)
        self.third_category = Category.objects.get(pk=4)
        self.expenditure = Expenditure.objects.create(category=self.category, 
            title='TFL',
            amount=14.28,
            date=self.today)
        self.other_expenditure = Expenditure.objects.create(category=self.other_category, 
            title='Cinema Tickets',
            amount=30.00,
            date=self.today)
        self.third_expenditure = Expenditure.objects.create(category=self.third_category, 
            title='Other',
            amount=2.85,
            date=self.today)

    def test_budget_list_url(self):
        self.assertEqual(self.url, '/budget_list/')

    def test_get_budget_list_when_logged_in(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget_list.html')

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_budget_list_shows_all_user_budgets(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        amount_spent = format(self.other_expenditure.amount, '.2f')
        
        self.assertContains(response, 'Overall')
        self.assertContains(response, f'£{self.third_expenditure.amount+self.other_expenditure.amount+self.expenditure.amount} out of £{self.user.budget.budget} spent')
        week_end_date = self.today - timedelta(days=self.today.weekday()) + relativedelta(days =+ 6)
        week_start_date = week_end_date - relativedelta(days =+ 6)
        self.assertContains(response, str(week_start_date))
        self.assertContains(response, str(week_end_date))
        
        self.assertContains(response, 'Transportation')
        self.assertContains(response, f'£{amount_spent} out of £{self.other_category.budget.budget} spent')
        month_start_date = date(self.today.year, self.today.month, 1)
        month_end_date = date(self.today.year, (self.today.month+1)%12, 1) - timedelta(days=1)
        self.assertContains(response, str(month_start_date))
        self.assertContains(response, str(month_end_date))
        
        self.assertContains(response, 'Entertainment')
        self.assertContains(response, f'£{self.expenditure.amount} out of £{self.category.budget.budget} spent')
        year_start_date = date(self.today.year,1,1)
        year_end_date = date(self.today.year+1, 1, 1) - timedelta(days=1)
        self.assertContains(response, str(year_start_date))
        self.assertContains(response, str(year_end_date))

        self.assertContains(response, 'Other')
        self.assertContains(response, f'£{self.third_expenditure.amount} out of £{self.third_category.budget.budget} spent')
        quarter = (self.today.month-1)//3 + 1 
        quarter_start_date = date(self.today.year, 3 * quarter - 2, 1)
        quarter_end_date = date(self.today.year, (3* quarter)%12 + 1, 1) + timedelta(days=-1) 
        self.assertContains(response, str(quarter_start_date))
        self.assertContains(response, str(quarter_end_date))

    def test_budget_list_does_not_show_other_user_budgets(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['budgets']), 4)
        self.assertEqual(len(self.user.get_categories()),3)
        self.assertNotContains(response, 'Utilities')
        