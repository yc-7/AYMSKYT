import pytz
from datetime import datetime, timedelta
from django.test import TestCase
from minted.models import User
from minted.models import Streak
from minted.views.general_user_views.point_system_views import update_streak
from django.test import RequestFactory


class CheckStreakTestCase(TestCase):
    
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]
   
    def setUp(self):
        self.user = User.objects.get(pk = 1)
        self.factory = RequestFactory()
    

    def test_increase_streak(self):
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=1)
        self.user.streak_data.last_login_time = window_start + timedelta(hours=1)
        self.user.streak_data.streak = 1
        self.user.streak_data.save()
        request = self.factory.get('/')
        request.user = self.user
        update_streak(request, self.user)
        self.assertEqual(self.user.streak_data.streak, 2)

    def test_reset_streak(self):
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=7)
        self.user.streak_data.last_login_time = window_start
        self.user.streak_data.streak = 3
        self.user.streak_data.save()
        request = self.factory.get('/')
        request.user = self.user
        update_streak(request, self.user)
        self.assertEqual(self.user.streak_data.streak, 1)
        
    def test_maintain_streak(self):
        now = datetime.now(pytz.utc)
        self.user.streak_data.last_login_time = now - timedelta(hours=12)
        self.user.streak_data.streak = 4
        self.user.streak_data.save()
        check_streak(self.user)
        self.assertEqual(self.user.streak_data.streak, 4)

   

