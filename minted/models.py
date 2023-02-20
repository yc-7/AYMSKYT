"""Models in the Minted app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django.utils.dateparse import parse_datetime
from operator import attrgetter
from itertools import groupby
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import datetime


class User(AbstractUser):
    """User model for authentication"""

    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True, blank=False)

    # Replaces the default django username with email for authentication
    username   = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return  self.first_name+" "+self.last_name


class Category(models.Model):
    """Model for expenditure categories"""

    user = models.ForeignKey(User, blank = False, on_delete= models.CASCADE)
    name = models.CharField(max_length = 50, blank = False)
    budget = models.DecimalField(default = 0, max_digits = 6, decimal_places = 2)

    def get_total_expenses_for_category(self, date_from, date_to):
        expenditures = Expenditure.objects.filter(category=self)
        expenses = expenditures.filter(date__gte = date_from).filter(date__lte = date_to)
        total = sum([expense.price for expense in expenses])

        return total

    def get_monthly_expenses_for_category(self, date_from, date_to):
        all_months = {}
        current_date = date_from.replace(day=1)
        while current_date <= date_to:
            year_month = current_date.strftime('%m-%Y')
            all_months[year_month] = 0
            current_date = current_date + relativedelta(months = 1)

        expenditures = Expenditure.objects.filter(category=self)
        expenses = expenditures.filter(date__gte = date_from).filter(date__lte = date_to).order_by('date')
        for expense in expenses:
            month_str = expense.date.strftime("%m-%Y")
            amount = Decimal(str(expense.price))
            if month_str in all_months:
                all_months[month_str]  += amount
            else:
                all_months[month_str] = amount

        return all_months
    
    def get_weekly_expenses_for_category(self, date_from, date_to):
        all_weeks = {}
        current_date = date_from.replace(day=1)
        
        while current_date <= date_to:
            year_month_week = current_date.strftime('%d-%m-%Y')
            all_weeks[year_month_week] = 0
            current_date = current_date + relativedelta(weeks = 1)
        
        def is_within_week(date_to_check, start_week):
            sunday_date = start_week + relativedelta(days = 6)
            falls_within_week = start_week <= date_to_check <= sunday_date
            return falls_within_week

        expenditures = Expenditure.objects.filter(category=self)
        expenses = expenditures.filter(date__gte = date_from).filter(date__lte = date_to).order_by('date')
        for expense in expenses:
            amount = Decimal(str(expense.price))

            for week_start_date in all_weeks:
                week_start_date_object = datetime.datetime.strptime(week_start_date, '%d-%m-%Y')
                if is_within_week(expense.date, week_start_date_object.date()):
                    all_weeks[week_start_date] += amount

        return all_weeks

class Expenditure(models.Model):
    """Model for expenditures"""

    user = models.ForeignKey(User, blank = False, on_delete= models.CASCADE)
    category = models.ForeignKey(Category, null = True, blank = True, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50, blank = False)
    price = models.DecimalField(default = 0, max_digits = 6, decimal_places = 2)
    date = models.DateField(blank = True)
    description = models.TextField(
        blank = True, 
        validators=[
            MaxLengthValidator(200),
        ]
    )
    receipt_image = models.FileField(upload_to='uploads/', blank = True)
    
