import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from django.db.models.query import QuerySet

def is_within_week(date_to_check: date, start_of_week: date) -> bool:
    """ Checks if a date is within a week """
    
    sunday_date = start_of_week + relativedelta(days = 6)
    falls_within_week = start_of_week <= date_to_check <= sunday_date
    return falls_within_week

def get_years_between_dates(date_from: date, date_to: date) -> dict:
    """
    Returns all years between two dates

    :return: A dictionary containing all years formatted 'YYYY' initialised with values of 0
    """
    all_years = {}
    current_date = date_from.replace(day = 1)
    while current_date <= date_to:
        year = current_date.strftime('%Y')
        all_years[year] = 0
        current_date = current_date + relativedelta(years = 1)

    return all_years

def get_months_between_dates(date_from: date, date_to: date) -> dict:
    """
    Returns all months between two dates

    :return: A dictionary containing all months formatted 'MM-YYYY' initialised with values of 0
    """
    all_months = {}

    current_date = date_from.replace(day=1)
    while current_date <= date_to:
        year_month = current_date.strftime('%m-%Y')
        all_months[year_month] = 0
        current_date = current_date + relativedelta(months = 1)
    
    return all_months

def get_weeks_between_dates(date_from: date, date_to: date) -> dict:
    """
    Returns all weeks between two dates

    :return: A dictionary containing all weeks formatted 'DD-MM-YYYY' initialised with values of 0
    """
    all_weeks = {}

    current_date = date_from.replace(day=1)
    while current_date <= date_to:
        year_month_week = current_date.strftime('%d-%m-%Y')
        all_weeks[year_month_week] = 0
        current_date = current_date + relativedelta(weeks = 1)
    
    return all_weeks

def get_days_between_dates(date_from: date, date_to: date) -> dict:
    """
    Returns all days between two dates

    :return: A dictionary containing all days formatted 'DD-MM-YYYY' initialised with values of 0
    """
    all_days = {}

    current_date = date_from
    while current_date <= date_to:
        year_month_day = current_date.strftime('%d-%m-%Y')
        all_days[year_month_day] = 0
        current_date = current_date + relativedelta(days = 1)

    return all_days

def get_spending_for_years(years: dict, expenditures: QuerySet) -> dict:
    """
    Returns all spending for years and total spending based on expenditures

    :param years: dict of all years('YYYY') and their current total spending
    :param expenditures: Queryset of all expenditures that should be calculated
    :return: A dictionary containing all years formatted 'YYYY' with values of total spending amounts
    """
    for expense in expenditures:
            year_str = expense.date.strftime("%Y")
            amount = expense.amount

            years[year_str] = years.get(year_str, 0) + amount

    return years

def get_spending_for_months(months: dict, expenditures: QuerySet) -> dict:
    """
    Returns all spending for months and total spending based on expenditures

    :param months: dict of all months('MM-YYYY') and their current total spending
    :param expenditures: Queryset of all expenditures that should be calculated
    :return: A dictionary containing all months formatted 'MM-YYYY' with values of total spending amounts
    """
    for expense in expenditures:
        month_str = expense.date.strftime("%m-%Y")
        amount = expense.amount

        months[month_str] = months.get(month_str, 0) + amount

    return months

def get_spending_for_weeks(weeks: dict, expenditures: QuerySet) -> dict:
    """
    Returns all spending for weeks and total spending based on expenditures

    :param weeks: dict of all weeks('DD-MM-YYYY') and their current total spending
    :param expenditures: Queryset of all expenditures that should be calculated
    :return: A dictionary containing all weeks formatted 'DD-MM-YYYY' with values of total spending amounts
    """
    for expense in expenditures:
        amount = expense.amount

        for week_start_date in weeks:
            week_start_date_object = datetime.datetime.strptime(week_start_date, '%d-%m-%Y').date()
            if is_within_week(expense.date, week_start_date_object):
                weeks[week_start_date] += amount

    return weeks

def get_spending_for_days(days: dict, expenditures: QuerySet) -> dict:
    """
    Returns all spending for days and total spending based on expenditures

    :param days: dict of all days('DD-MM-YYYY') and their current total spending
    :param expenditures: Queryset of all expenditures that should be calculated
    :return: A dictionary containing all days formatted 'DD-MM-YYYY' with values of total spending amounts
    """
    for expense in expenditures:
        day_str = expense.date.strftime("%d-%m-%Y")
        amount = expense.amount

        days[day_str] = days.get(day_str, 0) + amount

    return days