import pytz
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from minted.models import Streak
from minted.views import check_streak
from django.urls import reverse


class CheckStreakTestCase(TestCase):
    
    fixtures = [
        'minted/tests/fixtures/default_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]
    
    # def setUp(self):
    #     self.user = User.objects.create_user(
    #         username='testuser', email='test@example.com', password='testpass')
    #     self.streak_data = Streak.objects.create(user=self.user)     
        
    def setUp(self):
        self.url = reverse('login')
        self.form_input = {
            'first_name': 'TestName',
            'last_name': 'TestLastname',
            'email': 'test@example.org',
        }
        self.user = User.objects.get(pk = 1)
        self.user.streak_data = Streak.objects.create(user=self.user)

    def test_increase_streak(self):
        # Set the last login time to within the streak window
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=1)
        self.streak_data.last_login_time = window_start
        self.streak_data.streak = 1
        self.streak_data.save()

        # Call the check_streak function
        check_streak(self.user)

        # Check that the streak count has increased
        self.assertEqual(self.streak_data.streak, 2)

    def test_reset_streak(self):
        # Set the last login time to outside the streak window
        now = datetime.now(pytz.utc)
        window_start = now - timedelta(days=7)
        self.streak_data.last_login_time = window_start
        self.streak_data.streak = 3
        self.streak_data.save()

        # Call the check_streak function
        check_streak(self.user)

        # Check that the streak count has been reset to 1
        self.assertEqual(self.streak_data.streak, 1)

    def test_create_streak_data(self):
        # Set the user's streak data to None
        self.user.streak_data = None
        self.user.save()

        # Call the check_streak function
        check_streak(self.user)

        # Check that a new StreakData object has been created for the user
        self.assertIsNotNone(self.user.streak_data)
        self.assertEqual(self.user.streak_data.streak, 1)

