import pytz
from datetime import datetime, timedelta
from django.test import TestCase
from minted.models import User
from minted.views import update_streak

from unittest.mock import MagicMock, patch



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
        update_streak(self.user)
        self.assertEqual(self.user.streak_data.streak, 2)
        
    def test_increase_streak_edge_case(self):
        
            # Set the initial last_login_time to one day ago at 23:59
        now = datetime.now(pytz.utc)
        one_day_ago = now - timedelta(days=2)
        initial_login_time = one_day_ago.replace(hour=23, minute=59, second=0, microsecond=0)

        print("Initial login time:", initial_login_time)

        # Set the user's initial streak data
        self.user.streak_data.streak = 3
        self.user.streak_data.last_login_time = initial_login_time

        # Mock the current time in the entire module
        with patch('minted.views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:
            # Set the mocked current time
            mock_datetime.now.return_value = initial_login_time + timedelta(minutes=1)

            update_streak(self.user)

            print("Last login time:", self.user.streak_data.last_login_time)

        # Check that the streak has increased to 4
        self.assertEqual(self.user.streak_data.streak, 4)

        # Mock the current time in the entire module
        with patch('minted.views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:
            # Set the mocked current time
            mock_datetime.now.return_value = initial_login_time + timedelta(days=1, minutes=1)

            update_streak(self.user)

            print("Last login time:", self.user.streak_data.last_login_time)
            print("Current time:", initial_login_time + timedelta(days=1, minutes=1))

        # Check that the streak has increased to 5
        self.assertEqual(self.user.streak_data.streak, 5)
        
    def test_reset_streak(self):
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=7)
        self.user.streak_data.streak = 3
        self.user.streak_data.last_login_time = window_start
        update_streak(self.user)
        self.assertEqual(self.user.streak_data.streak, 1)
        
    def test_maintain_streak(self):
        now = datetime.now(pytz.utc)
        self.user.streak_data.last_login_time = now - timedelta(hours=12)
        self.user.streak_data.streak = 4
        update_streak(self.user)
        self.assertEqual(self.user.streak_data.streak, 4)

   

