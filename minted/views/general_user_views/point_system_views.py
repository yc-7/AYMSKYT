from datetime import datetime, timedelta
import pytz

def reward_login_points(user):
    last_login = user.streak_data.last_login_time
    
    if last_login.date() < datetime.now().date():
         user.points += 5
         user.save()
 
def reward_streak_points(user):
    points_rewarded = (user.streak_data.streak % 7) * 10
    user.points += points_rewarded 
    user.save()

def update_streak(user):
    if user.is_superuser:
        return

    window_size=timedelta(days=1)
    last_login = user.streak_data.last_login_time
    time_since_last_login = datetime.now(pytz.utc) - last_login
    reward_login_points(user)

    user_has_missed_day = last_login is None or time_since_last_login >= 2 * window_size
    if user_has_missed_day:
        user.streak_data.streak = 1
    elif window_size <= time_since_last_login < 2 * window_size:
        user.streak_data.streak += 1
        reward_streak_points(user)

    user.streak_data.save()