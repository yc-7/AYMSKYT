from minted.models import *
from datetime import datetime, timedelta
from django.utils import timezone
import pytz


def reward_points_daily(request):
    user = request.user
    check_streak(user)
    
    last_awarded = user.points.timestamp.date()
    today = timezone.now().date()
    if last_awarded < today:
        if user.streak_data.streak == 7:
            reward_custom_points(request, 30)
        else:
            reward_custom_points(request, 10)
    
    #return render(request, 'dashboard.html', {'points': user_points})

        

def reward_custom_points(request, input_points):
    current_user = request.user
    current_user.points.points += input_points 
    current_user.points.save() 



def check_streak(user):
    
    now = datetime.now(pytz.utc)
    window_start = now - timedelta(days=1)
    last_login = user.streak_data.last_login_time
    print('last login:', last_login)
    print('window start:', window_start)

    if last_login is None or last_login.date() < now.date() and last_login < window_start:
        user.streak_data.streak = 1
        user.streak_data.last_login_time = user.last_login
        
    elif last_login.date() < now.date() and last_login >= window_start:
        user.streak_data.streak += 1
        user.streak_data.last_login_time = user.last_login

    user.streak_data.save()