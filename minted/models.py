"""Models in the Minted app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from django.core.validators import MaxLengthValidator
from django.core.validators import MaxLengthValidator, MinValueValidator
from .model_functions import *

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
    budget = models.DecimalField(default = 0, max_digits = 6, decimal_places = 2, validators=[MinValueValidator(0)])

    def get_expenditures_between_dates(self, date_from, date_to):
        expenditures = Expenditure.objects.filter(category=self)
        expenses = expenditures.filter(date__gte = date_from, date__lte = date_to).order_by('date')

        return expenses

    def get_total_expenses_for_category(self, date_from, date_to):
        expenses = self.get_expenditures_between_dates(date_from, date_to)
        total = sum([expense.price for expense in expenses])

        return total

    def get_yearly_expenses_for_category(self, date_from, date_to):
        all_years = get_years_between_dates(date_from, date_to)

        expenses = self.get_expenditures_between_dates(date_from, date_to)
        yearly_expenses = get_spending_for_years(all_years, expenses)

        return yearly_expenses

    def get_monthly_expenses_for_category(self, date_from, date_to):
        all_months = get_months_between_dates(date_from, date_to)

        expenses = self.get_expenditures_between_dates(date_from, date_to)
        monthly_expenses = get_spending_for_months(all_months, expenses)

        return monthly_expenses
    
    def get_weekly_expenses_for_category(self, date_from, date_to):
        all_weeks = get_weeks_between_dates(date_from, date_to)

        expenses = self.get_expenditures_between_dates(date_from, date_to)
        weekly_expenses = get_spending_for_weeks(all_weeks, expenses)

        return weekly_expenses
    
    def get_daily_expenses_for_category(self, date_from, date_to):
        all_days = get_days_between_dates(date_from, date_to)

        expenses = self.get_expenditures_between_dates(date_from, date_to)
        daily_expenses = get_spending_for_days(all_days, expenses)

        return daily_expenses

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

