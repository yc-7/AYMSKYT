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

        now = datetime.now(pytz.utc)
        one_day_ago = now - timedelta(days=1)
        initial_login_time = one_day_ago.replace(hour=23, minute=59, second=0, microsecond=0)

        self.user.streak_data.streak = 3
        self.user.streak_data.last_login_time = initial_login_time

        # Mock the current time to be 00:01 
        with patch('minted.views.general_user_views.point_system_views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:
            
            mock_datetime.now.return_value = initial_login_time + timedelta(minutes=2)
            update_streak(self.user)

        self.assertEqual(self.user.streak_data.streak, 4)
        
    def test_increase_streak_edge_case_2(self):

        now = datetime.now(pytz.utc)
        one_day_ago = now - timedelta(days=1)
        initial_login_time = one_day_ago.replace(hour=00, minute=00, second=1, microsecond=0) # eg. 20/03/2023 at 00:00:01

        self.user.streak_data.streak = 3
        self.user.streak_data.last_login_time = initial_login_time

        # Mock the current time to be eg. 21/03/2023 at 23:59:59 (1 second before the streak will reset)
        with patch('minted.views.general_user_views.point_system_views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:
            
            mock_datetime.now.return_value = (initial_login_time + timedelta(days= 1)).replace(hour=23, minute=59, second=59, microsecond=0)
            update_streak(self.user)

        self.assertEqual(self.user.streak_data.streak, 4)
        
    def test_increase_streak_last_day_of_month(self):
        
        # Set the initial last_login_time to last day of the month at 23:59
        now = datetime.now(pytz.utc)
        initial_login_time = now.replace(month = 2,day = 28, hour=23, minute=59, second=0, microsecond=0)

        self.user.streak_data.streak = 3
        self.user.streak_data.last_login_time = initial_login_time

        # Mock the current time to be 00:01 on the first day of the next month
        with patch('minted.views.general_user_views.point_system_views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:
            
            mock_datetime.now.return_value = initial_login_time + timedelta(minutes=2)
            update_streak(self.user)
            
    
        self.assertEqual(self.user.streak_data.streak, 4)

        
    def test_reset_streak(self):
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=3)
        self.user.streak_data.streak = 3
        self.user.streak_data.last_login_time = window_start
        update_streak(self.user)
        self.assertEqual(self.user.streak_data.streak, 1)
        
    def test_reset_streak_edge_case(self):
        
        now = datetime.now(pytz.utc)
        initial_login_time = now.replace(hour=23, minute=59, second=0, microsecond=0)

        self.user.streak_data.streak = 3
        self.user.streak_data.last_login_time = initial_login_time

        # Mock the current time to be 24h and 1 minute after initial login
        with patch('minted.views.general_user_views.point_system_views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:

            mock_datetime.now.return_value = initial_login_time + timedelta(days= 1, minutes=1)
            update_streak(self.user)

        self.assertEqual(self.user.streak_data.streak, 1)
        
    def test_maintain_streak(self):
        now = datetime.now(pytz.utc)
        initial_login_time = now.replace(hour=12, minute=00, second=0, microsecond=0)
        
        self.user.streak_data.last_login_time = initial_login_time
        self.user.streak_data.streak = 4
        
        #Mock the current time to be 3 hours after initial login
        with patch('minted.views.general_user_views.point_system_views.datetime', new=MagicMock(wraps=datetime)) as mock_datetime:
            
            mock_datetime.now.return_value = initial_login_time + timedelta(hours= 3)

            update_streak(self.user)
            self.assertEqual(self.user.streak_data.streak, 4)

   

