from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncQuarter
from ..models import *

class Budget:

    def __init__(self, name, spent, budget, start_date, end_date):
        self.name = name
        self.spent = spent
        self.budget = budget
        self.ninty_percentage_of_budget = round(float(budget) * 0.9, 2)
        self.spent_text = f"£{str(round(spent, 2))} out of £{str(budget)} spent"
        self.start_date = start_date
        self.end_date = end_date
        self.percentage_spent = round((float(spent) / float(budget))*100)

def total_spending_limit(filtered_expenditures, budget, timeframe):
    if timeframe == '/week':
        return filtered_expenditures.annotate(week=TruncWeek('date')).values('week').annotate(spent = Sum('amount')).order_by('week')
    if timeframe == '/month':
        return filtered_expenditures.annotate(month=TruncMonth('date')).values('month').annotate(spent = Sum('amount')).order_by('month')
    if timeframe == '/quarter':
        return filtered_expenditures.annotate(quarter=TruncQuarter('date')).values('quarter').annotate(spent = Sum('amount')).order_by('quarter')
    if timeframe == '/year':
        return filtered_expenditures.annotate(year=TruncYear('date')).values('year').annotate(spent = Sum('amount')).order_by('year')

def total_spending_limits_of_category(category):
    filtered_expenditures = Expenditure.objects.filter(category = category)
    timeframe = category.budget.timeframe
    budget = category.budget.budget
    return total_spending_limit(filtered_expenditures, budget, timeframe)

def total_spending_limits_of_user(user):
    filtered_expenditures = user.get_expenditures()
    timeframe = user.budget.timeframe
    budget = user.budget.budget
    return total_spending_limit(filtered_expenditures, budget, timeframe)

def get_week_end_date(today):
    return today - timedelta(days=today.weekday()) + relativedelta(days =+ 6)

def get_week_start_date(today):
    return get_week_end_date(today) - relativedelta(days =+ 6)

def get_month_start_date(today):
    return date(today.year, today.month, 1)

def get_month_end_date(today):
    return date(today.year, (today.month+1)%12, 1) - timedelta(days=1)

def get_quarter(today):
    return (today.month-1)//3 + 1

def get_quarter_start_date(today):
    quarter = get_quarter(today)
    return date(today.year, 3 * quarter - 2, 1)

def get_quarter_end_date(today):
    quarter = get_quarter(today)
    return date(today.year, (3* quarter)%12 + 1, 1) + timedelta(days=-1)

def get_year_start_date(today):
    return date(today.year,1,1)

def get_year_end_date(today):
    return date(today.year+1, 1, 1) - timedelta(days=1)

def get_current_spending(name, spending_limits, budget, timeframe):
    today = date.today()
    start_date = today
    end_date = today
    if timeframe == '/week':
        start_date = get_week_start_date(today)
        end_date = get_week_end_date(today)
        for week in spending_limits:
            if week['week'] == start_date:
                return Budget(name, week['spent'], budget,  str(start_date), str(end_date))
    if timeframe == '/month':
        start_date = get_month_start_date(today)
        end_date = get_month_end_date(today)
        for month in spending_limits:
            if month['month'] == start_date:
                return Budget(name, month['spent'], budget,  str(start_date), str(end_date))
    if timeframe == '/quarter':
        start_date = get_quarter_start_date(today)
        end_date = get_quarter_end_date(today)
        for quarter in spending_limits:
            if quarter['quarter'] == start_date:
                return Budget(name, quarter['spent'], budget,  str(start_date), str(end_date))
    if timeframe == '/year':
        start_date = get_year_start_date(today)
        end_date = get_year_end_date(today)
        for year in spending_limits:
            if year['year'] == start_date:
                return Budget(name, year['spent'], budget,  str(start_date), str(end_date))
    return Budget(name, 0, budget, str(start_date), str(end_date))

def current_category_limit(category):
    spending_limits = total_spending_limits_of_category(category)
    timeframe = category.budget.timeframe
    budget = category.budget.budget
    name = category.name
    return get_current_spending(name, spending_limits, budget, timeframe)

def current_user_limit(user):
    spending_limits = total_spending_limits_of_user(user)
    timeframe = user.budget.timeframe
    budget = user.budget.budget
    name = 'Overall'
    return get_current_spending(name, spending_limits, budget, timeframe)

def get_budgets(user, categories):
    all_budgets = []

    for category in categories:
        all_budgets.append(current_category_limit(category))
    if user.budget is not None:
        all_budgets.append(current_user_limit(user))

    return all_budgets
