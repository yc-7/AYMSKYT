"""Models in the Minted app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from .model_functions import *
from django.conf import settings

class Streak(models.Model):
        
    last_login_time = models.DateTimeField(blank = True, null= True)
    streak = models.IntegerField(
        default = 0, 
        validators= [
            MinValueValidator(0)
        ]
    )

TIMEFRAME = [
    ('/week', 'week'),
    ('/month', 'month'),
    ('/quarter', 'quarter'),
    ('/year', 'year'),
]

class SpendingLimit(models.Model):
    """Model for spending limits"""

    budget = models.DecimalField(max_digits = 12, decimal_places = 2, blank=False)
    timeframe = models.CharField(max_length=11, choices=TIMEFRAME, blank=False)

    def __str__(self):
        return ' £' + str(self.budget) + str(self.timeframe)
    


class Subscription(models.Model):
    """Model for subscription options"""

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
class NotificationSubscription(models.Model):
    """Model for user notification subscriptions"""
    FREQUENCY_CHOICES = (
        (1, 'Daily'),
        (7, 'Weekly'),
        (30, 'Monthly'),
    )

    frequency = models.IntegerField(choices=FREQUENCY_CHOICES, blank=True, null=True)
    subscriptions = models.ManyToManyField(Subscription, blank=True)

class User(AbstractUser):
    """User model for authentication"""

    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True, blank=False)
    streak_data = models.OneToOneField(Streak ,  null= True, blank= True,  on_delete=models.CASCADE)
    budget = models.OneToOneField(SpendingLimit, null= True, blank= True, on_delete=models.CASCADE)
    points = models.IntegerField(default = 10, validators= [MinValueValidator(0)], blank=False)
    notification_subscription = models.OneToOneField(NotificationSubscription, null=True, blank=True, on_delete=models.SET_NULL)

    # Replaces the default django username with email for authentication
    username   = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return  self.first_name+" "+self.last_name

    def get_categories(self):
        categories = Category.objects.filter(user=self)
        return categories

    def get_expenditures(self):
        expenditures = Expenditure.objects.filter(category__user=self)
        #expenditures = Expenditure.objects.filter(category__user=self).select_related('category') #this also works
        return expenditures
    



class Category(models.Model):
    """Model for expenditure categories"""

    user = models.ForeignKey(User, blank = False, on_delete= models.CASCADE)
    name = models.CharField(max_length = 50, blank = False)
    budget = models.OneToOneField(SpendingLimit, blank = False, on_delete=models.CASCADE)
    colour = models.CharField(max_length = 7, blank = True, null =True)

    def __str__(self):
        return self.name


    def get_expenditures(self):
        expenditures = Expenditure.objects.filter(category=self)
        return expenditures

    def get_expenditures_between_dates(self, date_from, date_to):
        expenditures = Expenditure.objects.filter(category=self)
        expenses = expenditures.filter(date__gte = date_from, date__lte = date_to).order_by('date')

        return expenses

    def get_total_expenses_for_category(self, date_from, date_to):
        expenses = self.get_expenditures_between_dates(date_from, date_to)
        total = sum([expense.amount for expense in expenses])

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

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    date = models.DateField()
    description = models.CharField(max_length = 200, blank = True)
    receipt = models.FileField(upload_to = settings.UPLOAD_DIR, blank = True)
