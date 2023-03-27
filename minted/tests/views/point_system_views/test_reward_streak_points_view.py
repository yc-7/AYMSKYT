from django.test import TestCase
from minted.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from minted.views.general_user_views.point_system_views import *

class TestViews(TestCase):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.user = User.objects.get(pk = 1)
        

    def test_reward_login_points(self):
        initial_points = self.user.points
        reward_login_points(self.user)
        self.assertEqual(self.user.points, initial_points + 5)


    def test_reward_no_streak_points_when_no_streak(self):
        initial_points = self.user.points
        reward_streak_points(self.user)
        self.assertEqual(self.user.points, initial_points + 0)


    def test_reward_streak_points(self):
        self.user.streak_data.streak = 6
        self.user.streak_data.save()
        initial_points = self.user.points
        reward_streak_points(self.user)
        self.assertEqual(self.user.points, initial_points + 60)


    def test_reward_streak_and_login_points_when_no_streak(self):
        initial_points = self.user.points
        reward_login_and_streak_points(self.user)
        self.assertEqual(self.user.points, initial_points + 5)


    def test_reward_streak_and_login_points_when_streak(self):
        self.user.streak_data.streak = 6
        initial_points = self.user.points
        reward_login_and_streak_points(self.user)
        self.assertEqual(self.user.points, initial_points + 65)


    def test_no_streak_or_login_points_when_login_within_a_day(self):
        self.user.streak_data.streak = 6
        self.user.streak_data.last_login_time = datetime.now()
        initial_points = self.user.points
        reward_login_and_streak_points(self.user)
        self.assertEqual(self.user.points, initial_points + 0)
        