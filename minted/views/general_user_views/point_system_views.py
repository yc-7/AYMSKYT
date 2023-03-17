from minted.models import *
from minted.views.budget_views import *  
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


def calculate_category_weightings(request, category, all_budgets):
    user = request.user
    user_total_budget = all_budgets[-1]
    if (user.budget.timeframe != '/year'):
        user_yearly_budget = standardise_timeframe(user)
    else:
        user_yearly_budget = user_total_budget.budget
   
    category_object = Category.objects.get(user = user.id, name = category.name)
    if category_object.budget.timeframe != '/year':
        category_yearly_budget = standardise_timeframe(category_object)
        weighting_of_category = category_yearly_budget / user_yearly_budget
    else:
        weighting_of_category = float(category.budget) / user_yearly_budget
    return weighting_of_category


def calculate_budget_points(request, all_budgets, category):
    total_budget_reward = 100
    weighting_of_category = calculate_category_weightings(request, category, all_budgets)
    points_reward = math.ceil(weighting_of_category * total_budget_reward)
    return points_reward

def is_today_a_end_date(request):
    categories = request.user.get_categories()
    all_budgets = generate_budget_list(request, categories)
    today = datetime.now().date()
    ends_today = []
    for category in all_budgets:
        today = False
        if today == category.end_date:
            today = True
        ends_today.append(today)
    return ends_today


def reward_budget_points(request):
    user = request.user
    categories = user.get_categories()
    all_budgets = generate_budget_list(request, categories)
    now = str(timezone.now().date())
    if (all_budgets is not None) and (len(all_budgets) > 1):
        for category in all_budgets[:-1]:
            if category.spent <= category.budget and now == category.end_date:
                reward_points = calculate_budget_points(request, all_budgets, category)
                user.points += reward_points
                user.save()

       

def update_streak(request, user):  
    window_size=timedelta(days=1)
    last_login = user.streak_data.last_login_time
    time_since_last_login = datetime.now(pytz.utc) - last_login

    if last_login is None or time_since_last_login >= 2 * window_size:
        user.streak_data.streak = 1
        user.streak_data.last_login_time = user.last_login
        reward_points_daily(request)
        ends_today = is_today_a_end_date(request)
        if ends_today.contains(True):
            reward_budget_points(request)
    elif window_size <= time_since_last_login < 2 * window_size:
        user.streak_data.streak += 1
        user.streak_data.last_login_time = user.last_login
        reward_points_daily(request)
        ends_today = is_today_a_end_date(request)
        if ends_today.contains(True):
            reward_budget_points(request)

    reward_budget_points(request)
        
    user.streak_data.save()