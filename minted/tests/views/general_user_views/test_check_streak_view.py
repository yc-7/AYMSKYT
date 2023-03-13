import pytz
from datetime import datetime, timedelta
from django.test import TestCase
from minted.models import User
from minted.models import Streak
from minted.views import check_streak
from django.urls import reverse


class CheckStreakTestCase(TestCase):
    
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]
   
    def setUp(self):
        self.user = User.objects.get(pk = 1)

    def test_increase_streak(self):

        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=1)
        self.user.streak_data.last_login_time = window_start
        self.user.streak_data.streak = 1
        self.user.streak_data.save()
        check_streak(self.user)
        self.assertEqual(self.user.streak_data.streak, 2)

    def test_reset_streak(self):
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=7)
        self.user.streak_data.last_login_time = window_start
        self.user.streak_data.streak = 3
        self.user.streak_data.save()
        check_streak(self.user)
        self.assertEqual(self.user.streak_data.streak, 1)

   

