from django.test import TestCase
from minted.models import User
from minted.views.general_user_views.point_system_views import *
from minted.views.budget_views_functions import Budget
from minted.tests.helpers import LoginRequiredTester
from unittest.mock import MagicMock, patch

class BudgetPointsTestViews(TestCase, LoginRequiredTester):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_third_user.json',
        "minted/tests/fixtures/default_spending_limit.json",
        "minted/tests/fixtures/default_categories.json"
    ]

    def setUp(self):
        self.user = User.objects.get(pk = 1)
        self.budget_dicts = [
            {
                'name': 'Other',
                'spent': 45,
                'budget': 50,
                'start_date': '2022-01-01',
                'end_date': str(timezone.now().date())
            },
            {
                'name': 'Overall',
                'spent': 700,
                'budget': 1000,
                'start_date': '2022-01-01',
                'end_date': str(timezone.now().date())
            }
        ]   
        self.category = Category.objects.get(pk = 4)
        self.other_category = Category.objects.get(pk = 1)

    def test_today_is_not_end_date(self):
        
        now = datetime.now(pytz.utc)
        one_year_ago = now - timedelta(days=365)
        
        with patch('minted.views.general_user_views.point_system_views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:
            mock_datetime.now.return_value = one_year_ago
            ends_today = user_has_budget_ending_today(self.user)
            
        self.assertFalse(ends_today)

    def test_user_has_budget_ending_today(self):
        self.assertTrue(user_has_budget_ending_today(self.user))

    
    def test_standardise_yearly_timeframe(self):
        yearly_budget = standardise_timeframe(self.other_category)
        self.assertEqual(yearly_budget, 1000)


    def test_standardise_quarterly_timeframe(self):
        yearly_budget = standardise_timeframe(self.category)
        self.assertEqual(yearly_budget, 400)


    def test_standardise_monthly_timeframe(self):
        self.category.budget.timeframe = "/month"
        yearly_budget = standardise_timeframe(self.category)
        self.assertEqual(yearly_budget, 1200)

    
    def test_standardise_weekly_timeframe(self):
        self.category.budget.timeframe = "/week"
        yearly_budget = standardise_timeframe(self.category)
        self.assertEqual(yearly_budget, 5200)


    def test_calculate_category_weightings(self):
        
        budget_objects = []

        for budget_dict in self.budget_dicts:
            budget_object = Budget(
                name=budget_dict['name'],
                spent=budget_dict['spent'],
                budget=budget_dict['budget'],
                start_date=budget_dict['start_date'],
                end_date=budget_dict['end_date']
            )
            budget_objects.append(budget_object)
        weighting_of_category = calculate_category_weightings(self.user, self.category, budget_objects)
        self.assertEqual(round(weighting_of_category, 2), 0.05)



    def test_calculate_budget_points(self):
        
        budget_objects = []

        for budget_dict in self.budget_dicts:
            budget_object = Budget(
                name=budget_dict['name'],
                spent=budget_dict['spent'],
                budget=budget_dict['budget'],
                start_date=budget_dict['start_date'],
                end_date=budget_dict['end_date']
            )
            budget_objects.append(budget_object)
        points_reward = calculate_budget_points(self.user, budget_objects, self.category)
        self.assertEqual(points_reward, 6)

    