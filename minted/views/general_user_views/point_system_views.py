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
    
    now = datetime.now(pytz.utc)
    window_start = now - timedelta(days=1)
    last_login = user.streak_data.last_login_time

    if (last_login is None) or (last_login.date() < now.date() and last_login < window_start):
        user.streak_data.streak = 1
        reward_points_daily(request)
        reward_budget_points(request)
    elif last_login.date() < now.date() and last_login >= window_start:
        user.streak_data.streak += 1
        reward_points_daily(request)
        reward_budget_points(request)

    reward_budget_points(request)

    user.streak_data.save()