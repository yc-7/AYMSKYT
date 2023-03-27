from datetime import datetime
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

    last_login = user.streak_data.last_login_time
    now = datetime.now(pytz.utc)

    days_since_last_login = now.day - last_login.day

    if days_since_last_login >= 2:
        user.streak_data.streak = 1
        user.streak_data.last_login_time = now
    
    elif days_since_last_login == 1 or days_since_last_login < 0:
        user.streak_data.streak += 1
        reward_streak_points(user)
        user.streak_data.last_login_time = now
        
    user.streak_data.save()
