from minted.views.budget_views.budget_views_functions import *  
from minted.models import *
import datetime
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
import math

def reward_streak_points(user):
    if (user.streak_data.streak % 7) == 0:
        points_rewarded = 70
    else:
        points_rewarded= (user.streak_data.streak % 7)
        
    user.points += points_rewarded 
    user.save()
    
def reward_login_points(user):
    points_rewarded = 5
    user.points += points_rewarded 
    user.save()

def standardise_timeframe(category):
    if (category.budget.timeframe == '/week'):
        yearly_budget = float(category.budget.budget) * 52
    elif (category.budget.timeframe == '/quarter'):
        yearly_budget = float(category.budget.budget) * 4
    elif (category.budget.timeframe == '/month'):
        yearly_budget = float(category.budget.budget) * 12
    elif (category.budget.timeframe == '/year'):
        yearly_budget = float(category.budget.budget)
    return yearly_budget

def calculate_category_weightings(user, category, all_budgets):
    user_yearly_budget = standardise_timeframe(user)
    category_object = Category.objects.get(user = user.id, name = category.name)
    category_yearly_budget = standardise_timeframe(category_object)
    weighting_of_category = category_yearly_budget / user_yearly_budget
    return weighting_of_category

def calculate_budget_points(user, all_budgets, category):
    total_budget_reward = 100
    weighting_of_category = calculate_category_weightings(user, category, all_budgets)
    points_reward = math.ceil(weighting_of_category * total_budget_reward)
    return points_reward

def reward_budget_points(user):
    categories = user.get_categories()
    all_budgets = get_budgets(user, categories)
    today = str(timezone.now().date())

    if not all_budgets:
        return
    
    for category_budget in all_budgets[:-1]:
        within_budget = category_budget.spent <= category_budget.budget
        today_is_budget_end_date = today == category_budget.end_date
        if within_budget and today_is_budget_end_date:
            reward_points = calculate_budget_points(user, all_budgets, category_budget)
            user.points += reward_points
            user.save()

def user_has_budget_ending_today(user):
    categories = user.get_categories()
    all_budgets = get_budgets(user, categories)
    today = str(datetime.now().date())

    for category in all_budgets:
        if today == category.end_date:
            return True
    return False
    
def update_streak(user):
    if user.is_superuser:
        return

    last_login = user.streak_data.last_login_time.date()
    now = datetime.now(pytz.utc).date()

    days_since_last_login = (now - last_login).days

    if days_since_last_login >= 2:
        user.streak_data.streak = 1
        reward_login_points(user)
    
    elif days_since_last_login == 1:
        user.streak_data.streak += 1
        reward_streak_points(user)
        reward_login_points(user)
    
    else:
        return
    
    user.streak_data.last_login_time = datetime.now(pytz.utc)
    user.streak_data.save()
