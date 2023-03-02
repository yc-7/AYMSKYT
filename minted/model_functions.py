import datetime
from dateutil.relativedelta import relativedelta

def is_within_week(date_to_check, start_week):
    sunday_date = start_week + relativedelta(days = 6)
    falls_within_week = start_week <= date_to_check <= sunday_date
    return falls_within_week

def get_years_between_dates(date_from, date_to):
    all_years = {}
    current_date = date_from.replace(day = 1)
    while current_date <= date_to:
        year = current_date.strftime('%Y')
        all_years[year] = 0
        current_date = current_date + relativedelta(years = 1)

    return all_years

def get_months_between_dates(date_from, date_to):
    all_months = {}

    current_date = date_from.replace(day=1)
    while current_date <= date_to:
        year_month = current_date.strftime('%m-%Y')
        all_months[year_month] = 0
        current_date = current_date + relativedelta(months = 1)
    
    return all_months

def get_weeks_between_dates(date_from, date_to):
    all_weeks = {}

    current_date = date_from.replace(day=1)
    while current_date <= date_to:
        year_month_week = current_date.strftime('%d-%m-%Y')
        all_weeks[year_month_week] = 0
        current_date = current_date + relativedelta(weeks = 1)
    
    return all_weeks

def get_days_between_dates(date_from, date_to):
    all_days = {}

    current_date = date_from
    while current_date <= date_to:
        year_month_day = current_date.strftime('%d-%m-%Y')
        all_days[year_month_day] = 0
        current_date = current_date + relativedelta(days = 1)

    return all_days

def get_spending_for_years(years, expenditures):
    for expense in expenditures:
            year_str = expense.date.strftime("%Y")
            amount = expense.amount

            years[year_str] = years.get(year_str, 0) + amount

    return years

def get_spending_for_months(months, expenditures):
    for expense in expenditures:
        month_str = expense.date.strftime("%m-%Y")
        amount = expense.amount

        months[month_str] = months.get(month_str, 0) + amount

    return months

def get_spending_for_weeks(weeks, expenditures):
    for expense in expenditures:
        amount = expense.amount

        for week_start_date in weeks:
            week_start_date_object = datetime.datetime.strptime(week_start_date, '%d-%m-%Y').date()
            if is_within_week(expense.date, week_start_date_object):
                weeks[week_start_date] += amount

    return weeks

def get_spending_for_days(days, expenditures):
    for expense in expenditures:
        day_str = expense.date.strftime("%d-%m-%Y")
        amount = expense.amount

        days[day_str] = days.get(day_str, 0) + amount

    return days