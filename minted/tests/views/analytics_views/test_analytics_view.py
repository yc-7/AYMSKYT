from django.test import TestCase
from django.urls import reverse
from minted.forms import TimeFrameForm
from minted.models import User, Category
from minted.tests.helpers import reverse_with_next
import datetime

class AnalyticsViewTest(TestCase):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        "minted/tests/fixtures/default_categories.json",
        "minted/tests/fixtures/default_expenditures.json"
    ]

    def setUp(self):
        self.url = reverse('view_analytics')

        self.form_input = {
            'start_date': datetime.date(2023, 1, 1),
            'end_date': datetime.date(2024, 1, 1),
            'time_interval': 'monthly',
        }
        self.user = User.objects.get(pk = 1)


    def test_analytics_url(self):
        self.assertEqual(self.url,'/analytics/')
    
    def test_get_analytics(self):
        self.client.login(email=self.user.email, password="Password123")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analytics.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TimeFrameForm))

        one_year_from_today = datetime.date.today() - datetime.timedelta(days=365)
        self.assertTrue(form['start_date'], datetime.date.today())
        self.assertTrue(form['end_date'], one_year_from_today)

    def test_get_analytics_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_invalid_dates(self):
        self.client.login(email=self.user.email, password="Password123")

        self.form_input['start_date'] = datetime.date(2025, 1, 1)

        response = self.client.post(self.url, self.form_input)

        form = response.context['form']
        one_year_from_today = datetime.date.today() - datetime.timedelta(days=365)
        self.assertTrue(form['start_date'], datetime.date.today())
        self.assertTrue(form['end_date'], one_year_from_today)

        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors.keys())       

    def test_post_valid_dates(self):
        self.client.login(email=self.user.email, password="Password123")

        response = self.client.post(self.url, self.form_input)

        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertTrue(form['start_date'], datetime.date(2023, 1, 1))
        self.assertTrue(form['end_date'], datetime.date(2024, 1, 1))

        pie_chart_data = response.context['category_pie_chart_data'].get('data')
        self.assertTrue(len(pie_chart_data), 2)

        category_line_chart_datasets = response.context['category_line_chart_data'].get('datasets')
        self.assertTrue(len(category_line_chart_datasets), 2)

        all_spending_line_chart_datasets = response.context['all_spending_line_chart_data'].get('datasets')
        self.assertTrue(len(all_spending_line_chart_datasets), 2)

        
    def test_user_with_no_categories_renders_no_charts(self):
        self.client.login(email=self.user.email, password="Password123")
        Category.objects.filter(user = self.user).delete()
        
        response = self.client.post(self.url, self.form_input)

        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertTrue(form['start_date'], datetime.date(2023, 1, 1))
        self.assertTrue(form['end_date'], datetime.date(2024, 1, 1))

        self.assertTrue('category_pie_chart_data' not in response.context)
        self.assertTrue('category_line_chart_data' not in response.context)
        self.assertTrue('all_spending_line_chart_data' not in response.context)
