"""Models in the Minted app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from .user_manager import UserManager
from django.core.validators import MinValueValidator
from .model_functions import *
import datetime
from random import randint
import random
from django.core.files import File
from io import BytesIO
import segno
import os
from django.db import IntegrityError
from django.conf import settings
from string import ascii_uppercase

class Streak(models.Model):
        
    last_login_time = models.DateTimeField(blank = True, null= True, auto_now_add = True)
    streak = models.IntegerField(
        default = 1, 
        validators= [MinValueValidator(0),]
    )

class SpendingLimit(models.Model):
    """Model for spending limits"""

    TIMEFRAME = [
    ('/week', 'week'),
    ('/month', 'month'),
    ('/quarter', 'quarter'),
    ('/year', 'year'),
]

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
    friends = models.ManyToManyField('self', symmetrical ='False', blank = True)


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


class FriendRequest(models.Model):
	from_user = models.ForeignKey(User, related_name = 'from_user', on_delete = models.CASCADE)
	to_user = models.ForeignKey(User, related_name = 'to_user', on_delete = models.CASCADE)
	is_active = models.BooleanField(blank = False, null = False, default = True)

    
class Category(models.Model):
    """Model for expenditure categories"""

    user = models.ForeignKey(User, blank = False, on_delete= models.CASCADE)
    name = models.CharField(max_length = 50, blank = False)
    budget = models.OneToOneField(SpendingLimit, blank = False, on_delete=models.CASCADE)
    colour = models.CharField(max_length = 7, blank = True, null =True)

    class Meta:
        unique_together = ('user', 'name')

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


class RewardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expiry_date__gte = datetime.date.today())

class RewardBrandManager(models.Manager):
    def get_queryset(self, brand):
        return super().get_queryset().filter(brand_name = brand)

class Reward(models.Model):
    """Model for rewards"""

    CODE_TYPE_CHOICES = [
        ('qr', 'QR Code'),
        ('random', 'Randomly Generated Code'),
    ]

    brand_name = models.CharField(max_length = 50, blank = False)
    points_required = models.IntegerField(blank = False, validators = [MinValueValidator(1)])
    reward_id = models.CharField(max_length = 6, unique = True, blank = False)
    expiry_date = models.DateField(blank = False)
    description = models.TextField(max_length = 300, blank = False)
    cover_image = models.FileField(upload_to = settings.REWARDS_DIR, blank = True)
    code_type = models.CharField(max_length = 6, choices = CODE_TYPE_CHOICES, blank=False, default = 'random')
    user_limit = models.IntegerField(blank = True, null = True, validators = [MinValueValidator(0)])


    objects = RewardManager()
    same_brand = RewardBrandManager()

    def save(self, *args, **kwargs):
        if not self.reward_id:
            self.reward_id = self._create_reward_id()
        return super(Reward, self).save(*args, **kwargs)

    def _create_reward_id(self):
        brands = Reward.same_brand.get_queryset(self.brand_name).count()
        next_id = brands + 1
        format_id = f'{next_id:03}'
        full_id = self.brand_name[:3].replace(" ", "").upper() + format_id
        return full_id

    def __str__(self):
        return self.brand_name.lower().replace(" ", "-")


class RewardClaimManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(reward_type__expiry_date__gte=datetime.date.today())

class RewardClaim(models.Model):
    """Model for reward claims made by users"""

    claim_code = models.CharField(max_length = 10, blank = True, null = True, unique = True)
    claim_qr = models.FileField(upload_to = settings.REWARDS_DIR, blank = True)
    reward_type = models.ForeignKey(Reward, blank = False, on_delete = models.CASCADE)
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)

    def save(self, *args, **kwargs):
        if self.claim_qr != True or self.claim_code is None:
            if self.reward_type.code_type == 'qr':
                self.claim_qr = self._create_claim_qr()
            else:
                unique = False
                while (unique == False):
                    try:
                        if not self.claim_code:
                            self.claim_code = self._create_claim_code()
                            unique = True
                    except IntegrityError as e:
                        unique = False
        return super(RewardClaim, self).save(*args, **kwargs)
    
    def _create_claim_qr(self):
        qr_name = f'{self._create_claim_code}{self.reward_type.reward_id}_qr'
        qr = segno.make_qr(qr_name)
        qr_buffer = BytesIO()
        qr.save(qr_buffer, scale=10, kind='svg')
        qr_file = File(qr_buffer, name=f"{qr_name}.svg")
        qr_file.seek(0)
        return qr_file

    def _create_claim_code(self):
        full_id = 'MINT' + self.choose_digits(randint(1,2)) + self.choose_letters(randint(1,3)) + str(randint(0,9))
        return full_id

    def choose_letters(self, num):
        letters = ''
        for n in range(num):
            letters += random.choice(ascii_uppercase)
        return letters

    def choose_digits(self, num):
        digits = ''
        for n in range(num):
            digits += str(randint(0, 9))
        return digits



