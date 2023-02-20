"""Models in the Minted app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django.utils.dateparse import parse_datetime
from operator import attrgetter
from itertools import groupby
from collections import defaultdict
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
        expenses_by_month = {}
        

        expenditures = Expenditure.objects.filter(category=self)
        expenses = expenditures.filter(date__gte = date_from).filter(date__lte = date_to).order_by('date')
        for expense in expenses:
            month_str = expense.date.strftime("%B %Y")
            amount = Decimal(str(expense.price))
            if month_str in expenses_by_month:
                expenses_by_month[month_str]  += amount
            else:
                expenses_by_month[month_str] = amount

        return expenses_by_month

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
    
