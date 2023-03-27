from django.test import TestCase
from minted.models import User
from minted.views.general_user_views.point_system_views import *
from minted.views.budget_views_functions import Budget


class BudgetPointsTestViews(TestCase):

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


    def test_standardise_timeframe(self):
        yearly_budget = standardise_timeframe(self.other_category)
        self.assertEqual(yearly_budget, 7800)



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
        self.assertEqual(round(weighting_of_category, 2), 0.6)



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
        self.assertEqual(points_reward, 60)

    