from django.test import TestCase
from django.utils import timezone
from minted.models import Streak
from datetime import timedelta

class StreakModelTests(TestCase):
    
    def test_streak_default_value(self):
        
        streak = Streak.objects.create()
        self.assertEqual(streak.streak, 1)

    def test_streak_min_value(self):
        
        streak = Streak.objects.create(streak=0)
        self.assertEqual(streak.streak, 0)
        
    def test_last_login_time_auto_now_add(self):
       
        streak = Streak.objects.create()
        now = timezone.now()
        self.assertAlmostEqual(streak.last_login_time, now, delta=timedelta(seconds=1))

    def test_streak_update(self):
        
        streak = Streak.objects.create()
        new_streak_value = 5
        streak.streak = new_streak_value
        streak.save()
        self.assertEqual(streak.streak, new_streak_value)
