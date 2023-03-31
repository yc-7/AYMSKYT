from django.test import TestCase
from minted.models import User
from datetime import datetime
from minted.views.general_user_views.point_system_views import *
from minted.tests.helpers import LoginRequiredTester

class StreakPointsTestViews(TestCase, LoginRequiredTester):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.user = User.objects.get(pk = 1)
    
    def test_reward_login_points(self):
        initial_points = self.user.points
        update_streak(self.user)
        self.assertEqual(self.user.points, initial_points + 5)


    def test_reward_streak_points(self):
        
        self.user.points = 0
        initial_points = self.user.points
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=1)
        self.user.streak_data.last_login_time = window_start
        self.user.streak_data.streak = 6
        update_streak(self.user)
        self.assertEqual(self.user.points, initial_points + 75) # 70 for the streak and 5 for daily login

    
    def test_logged_in_today(self):

        initial_points = self.user.points
        now = datetime.now(pytz.utc)
        self.user.streak_data.last_login_time = now
        self.user.streak_data.streak = 6
        update_streak(self.user)
        self.assertEqual(self.user.points, initial_points) 
        