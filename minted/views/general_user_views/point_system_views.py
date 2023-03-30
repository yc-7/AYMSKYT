from minted.views.budget_views import *  
from minted.models import *
import datetime
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
import math

def reward_login_points(user):
    user.points += 5
    user.save()
 
def reward_streak_points(user):
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


def calculate_category_weightings(user, category, all_budgets):
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


def calculate_budget_points(user, all_budgets, category):
    total_budget_reward = 100
    weighting_of_category = calculate_category_weightings(user, category, all_budgets)
    points_reward = math.ceil(weighting_of_category * total_budget_reward)
    return points_reward

def reward_budget_points(user):
    categories = user.get_categories()
    all_budgets = generate_budget_list(user, categories)
    now = str(timezone.now().date())
    if (all_budgets is not None) and (len(all_budgets) > 1):
        for category in all_budgets[:-1]:
            if category.spent <= category.budget and now == category.end_date:
                reward_points = calculate_budget_points(user, all_budgets, category)
                user.points += reward_points
                user.save()

def is_today_a_end_date(user):
    categories = user.get_categories()
    all_budgets = generate_budget_list(user, categories)
    today = datetime.now().date()
    ends_today = []
    for category in all_budgets:
        is_today = False
        if today == category.end_date:
            is_today = True
        ends_today.append(is_today)
    return ends_today


def reward_login_and_streak_points(user):
    if user.streak_data is not None:
        last_login = user.streak_data.last_login_time
    
        if last_login.date() < datetime.now().date() and (not user.is_superuser):
            reward_login_points(user)
            reward_streak_points(user)
    


def update_streak(user):
    if user.is_superuser:
        return

    last_login = user.streak_data.last_login_time.date()
    now = datetime.now(pytz.utc).date()

    days_since_last_login = (now - last_login).days

    if days_since_last_login >= 2:
        user.streak_data.streak = 1
        user.streak_data.last_login_time = datetime.now(pytz.utc)
    
    elif days_since_last_login == 1:
        user.streak_data.streak += 1
        reward_streak_points(user)
        user.streak_data.last_login_time = datetime.now(pytz.utc)
        
    user.streak_data.save()
