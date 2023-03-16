from minted.models import *
from minted.views.budget_views import *  
from minted.views.general_user_views.point_system_view_function import all_budgets
import datetime
from datetime import datetime, timedelta
from django.utils import timezone
import pytz



def reward_points_daily(request):
    user = request.user
    points_rewarded = (user.streak_data.streak % 7) * 10
    user.points += points_rewarded 
    user.save()

def calculate_budget_points(request, total_user_budget):
    user = request.user
    total_budget_reward = 100
    for category in all_budgets[:-1]:
        weighting_of_category = category.budget / total_user_budget
        now = str(timezone.now().date())
        if (now == category.end_date) and (category.spent <= category.budget):
            user.points += (weighting_of_category * total_budget_reward)
            user.save()


def reward_budget_points(request):
    budget_list(request)
    user = request.user

    if (all_budgets is not None) and (len(all_budgets) > 1):
        total_user_budget = all_budgets[-1]
        sum_of_category_budgets = 0
        for category in all_budgets[:-1]:
            sum_of_category_budgets += category.budget

        if sum_of_category_budgets <= total_user_budget.budget:
            calculate_budget_points(request, total_user_budget.budget)
        else:
            calculate_budget_points(request, sum_of_category_budgets)


def update_streak(request, user):
    

    window_size=timedelta(days=1)
    last_login = user.streak_data.last_login_time
    time_since_last_login = datetime.now(pytz.utc) - last_login

    if last_login is None or time_since_last_login >= 2 * window_size:
        user.streak_data.streak = 1
        user.streak_data.last_login_time = user.last_login
        reward_points_daily(request)
        reward_budget_points(request)
    elif window_size <= time_since_last_login < 2 * window_size:
        user.streak_data.streak += 1
        user.streak_data.last_login_time = user.last_login
        reward_points_daily(request)
        reward_budget_points(request)
        
    
    reward_budget_points(request)

    user.streak_data.save()