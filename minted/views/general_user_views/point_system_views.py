from minted.models import *
from minted.views.budget_views import *  
from minted.views.general_user_views.point_system_view_function import all_budgets
import datetime
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
import math

def reward_points_daily(request):
    user = request.user
    points_rewarded = (user.streak_data.streak % 7) * 10
    user.points += points_rewarded 
    user.save()

def standardise_timeframe(category):
    if (category.budget.timeframe == '/week'):
        yearly_budget = float(category.budget.budget) * 52
    elif (category.budget.timeframe == '/quarter'):
        yearly_budget = float(category.budget.budget) * 4
    elif (category.budget.timeframe == '/month'):
        yearly_budget = float(category.budget.budget) * 12
    return yearly_budget


def calculate_category_weightings(request, category):
    user = request.user
    user_total_budget = all_budgets[-1]
    if (user.budget.timeframe != '/year'):
        user_yearly_budget = standardise_timeframe(user)
    else:
        user_yearly_budget = user_total_budget.budget
   
    category_object = Category.objects.get(user = user.id, name = category.name)
    if category_object.budget.timeframe != '/year':
        yearly_budget = standardise_timeframe(request, category_object)
        weighting_of_category = yearly_budget / user_yearly_budget
    else:
        weighting_of_category = float(category.budget) / user_yearly_budget
    return weighting_of_category


def calculate_budget_points(request):
    user = request.user
    total_budget_reward = 100
    for category in all_budgets[:-1]:
        weighting_of_category = calculate_category_weightings(request, category)
        now = str(timezone.now().date())
        
        if (now == category.end_date) and (category.spent <= category.budget):
            points_reward = math.ceil(weighting_of_category * total_budget_reward)
            user.points += points_reward
            user.save()

def is_today_a_end_date():
    today = datetime.now().date()
    ends_today = []
    for category in all_budgets:
        today = False
        if today == category.end_date:
            today = True
        ends_today.append(today)
    return ends_today


def reward_budget_points(request):
    budget_list(request)
    if (all_budgets is not None) and (len(all_budgets) > 1):
        calculate_budget_points(request)
       

def update_streak(request, user):  
    window_size=timedelta(days=1)
    last_login = user.streak_data.last_login_time
    time_since_last_login = datetime.now(pytz.utc) - last_login

    if last_login is None or time_since_last_login >= 2 * window_size:
        user.streak_data.streak = 1
        user.streak_data.last_login_time = user.last_login
        reward_points_daily(request)
        ends_today = is_today_a_end_date()
        if ends_today.contains(True):
            reward_budget_points(request)
    elif window_size <= time_since_last_login < 2 * window_size:
        user.streak_data.streak += 1
        user.streak_data.last_login_time = user.last_login
        reward_points_daily(request)
        ends_today = is_today_a_end_date()
        if ends_today.contains(True):
            reward_budget_points(request)
        
    user.streak_data.save()