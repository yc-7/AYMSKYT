from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncQuarter
from ..models import *

class Budget:

    def __init__(self, name, remaining, start_date, end_date):
        self.name = name
        self.remaining = remaining
        self.start_date = start_date
        self.end_date = end_date

def total_spending_limit(filtered_expenditures, budget, timeframe):
    if timeframe == '/week':
        return filtered_expenditures.annotate(week=TruncWeek('date')).values('week').annotate(remaining = budget - Sum('price')).order_by('week')
    if timeframe == '/month':
        return filtered_expenditures.annotate(month=TruncMonth('date')).values('month').annotate(remaining = budget - Sum('price')).order_by('month')
    if timeframe == '/quarter':
        return filtered_expenditures.annotate(quarter=TruncQuarter('date')).values('quarter').annotate(remaining = budget - Sum('price')).order_by('quarter')
    if timeframe == '/year':
        return filtered_expenditures.annotate(year=TruncYear('date')).values('year').annotate(remaining = budget - Sum('price')).order_by('year')

def total_spending_limits_of_category(category):
    filtered_expenditures = Expenditure.objects.filter(category = category)
    timeframe = category.budget.timeframe
    budget = category.budget.budget
    return total_spending_limit(filtered_expenditures, budget, timeframe)

def total_spending_limits_of_user(user):
    filtered_expenditures = Expenditure.objects.filter(user=user)
    timeframe = user.budget.timeframe
    budget = user.budget.budget
    return total_spending_limit(filtered_expenditures, budget, timeframe)

def current_spending_limit(name, all_limits, budget, timeframe):
    today = date.today()
    start_date = today
    end_date = today
    if timeframe == '/week':
        end_date = today - timedelta(days=today.isocalendar().weekday) + relativedelta(days =+ 7)
        start_date = end_date - relativedelta(days =+ 6)
        for week in all_limits:
            if week['week'] == start_date:
                return Budget(name, '£' + str(week['remaining']) + ' out of £' + str(budget) + ' remaining ', str(start_date), str(end_date))
    if timeframe == '/month':
        start_date = date(today.year, today.month, 1)
        end_date = date(today.year, (today.month+1)%12, 1) - timedelta(days=1)
        for month in all_limits:
            if month['month'] == start_date:
                return Budget(name, '£' + str(month['remaining']) + ' out of £' + str(budget) + ' remaining ', str(start_date), str(end_date))
    if timeframe == '/quarter':
        quarter = (today.month-1)//3 + 1
        start_date = date(today.year, 3 * quarter - 2, 1)
        end_date = date(today.year, (3* quarter)%12 + 1, 1) + timedelta(days=-1)
        for quarter in all_limits:
            if quarter['quarter'] == start_date:
                return Budget(name, '£' + str(quarter['remaining']) + ' out of £' + str(budget) + ' remaining ', str(start_date), str(end_date))
    if timeframe == '/year':
        start_date = date(today.year,1,1)
        end_date = date(today.year+1, 1, 1) - timedelta(days=1)
        for year in all_limits:
            if year['year'] == start_date:
                return Budget(name, '£' + str(year['remaining']) + ' out of £' + str(budget) + ' remaining ', str(start_date), str(end_date))
    return Budget(name, '£' + str(budget) + ' out of £' + str(budget) + ' remaining ', str(start_date), str(end_date))

def current_category_limit(category):
    all_limits = total_spending_limits_of_category(category)
    timeframe = category.budget.timeframe
    budget = category.budget.budget
    name = category.name
    return current_spending_limit(name, all_limits, budget, timeframe)

def current_user_limit(user):
    all_limits = total_spending_limits_of_user(user)
    timeframe = user.budget.timeframe
    budget = user.budget.budget
    name = 'Overall'
    return current_spending_limit(name,all_limits, budget, timeframe)