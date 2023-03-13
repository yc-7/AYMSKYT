from minted.models import *
from datetime import datetime, timedelta
from django.utils import timezone
import pytz


def reward_points_daily(request):
    user = request.user
    points_rewarded = (user.streak_data.streak % 7) * 10
    user.points += points_rewarded 
    user.save()



def update_streak(request, user):
    
    now = datetime.now(pytz.utc)
    window_start = now - timedelta(days=1)
    last_login = user.streak_data.last_login_time
    print('last login:', last_login)
    print('window start:', window_start)

    if (last_login is None) or (last_login.date() < now.date() and last_login < window_start):
        user.streak_data.streak = 1
        reward_points_daily(request)
    elif last_login.date() < now.date() and last_login >= window_start:
        user.streak_data.streak += 1
        reward_points_daily(request)

    user.streak_data.save()