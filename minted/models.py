"""Models in the Minted app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from .user_manager import UserManager
from .model_functions import *
import datetime
from random import randint
from django.conf import settings

TIMEFRAME = [
    ('/week', 'week'),
    ('/month', 'month'),
    ('/quarter', 'quarter'),
    ('/year', 'year'),
]

class SpendingLimit(models.Model):
    """Model for spending limits"""

    budget = models.DecimalField(default = None, max_digits = 12, decimal_places = 2, blank=False)
    timeframe = models.CharField(max_length=11, choices=TIMEFRAME, blank=False)

    def __str__(self):
        return ' £' + str(self.budget) + str(self.timeframe)

class User(AbstractUser):
    """User model for authentication"""

    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True, blank=False)
    budget = models.OneToOneField(SpendingLimit, null= True, blank= True, on_delete=models.CASCADE)

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

    category = models.ForeignKey(Category, null = True, blank = True, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    amount = models.DecimalField(default = 0, max_digits = 6, decimal_places = 2)
    date = models.DateField()
    description = models.CharField(max_length = 200, blank = True)
    receipt = models.FileField(upload_to = settings.UPLOAD_DIR, blank = True)

class RewardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expiry_date__gte = datetime.date.today())

class Reward(models.Model):
    """Model for rewards"""

    brand_name = models.CharField(max_length = 50, blank = False)
    points_required = models.IntegerField(blank = False, validators = [MinValueValidator(1)])
    reward_id = models.CharField(max_length = 6, unique = True, blank = False)
    expiry_date = models.DateField(blank = False)
    description = models.TextField(max_length = 300, blank = False)

    objects = RewardManager()

    def save(self, *args, **kwargs):
        if not self.reward_id:
            self.reward_id = self._create_reward_id()
        super(Reward, self).save(*args, **kwargs)

    def _create_reward_id(self):
        brand_code = self.brand_name[:3].replace(" ", "").upper()
        random_digits = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        return brand_code + random_digits

class RewardsClaimManager(models.Manager):
    def get_queryset(self):
        pass

class RewardClaim(models.Model):
    """Model for reward claims made by users"""

    claim_code = models.CharField(max_length = 6, blank = True)
    reward_type = models.ForeignKey(Reward, blank = False, on_delete = models.CASCADE)
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.claim_code:
            self.claim_code = self._create_claim_code()
        super(RewardClaim, self).save(*args, **kwargs)

    def _create_claim_code(self):
        pass

