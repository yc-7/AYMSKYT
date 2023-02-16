"""Models in the Minted app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
from django.utils import timezone
from django.core.validators import MaxLengthValidator

TIMEFRAME = [
    ('/week', 'week'),
    ('/month', 'month'),
    ('/quarter', 'quarter'),
    ('/year', 'year'),
]
#update spending limits whenever user logs in
class SpendingLimit(models.Model):
    #remaining_budget = models.DecimalField(default = None, max_digits = 12, decimal_places = 2, blank=False)
    budget = models.DecimalField(default = None, max_digits = 12, decimal_places = 2, blank=False)
    #limit
    timeframe = models.CharField(max_length=11, choices=TIMEFRAME, blank=True)
    #start_date = models.DateField(default = None, blank=False)
    #end_date = models.DateField(default = None, blank=False)

    # def __str__(self):
    #     return 'You have ' + str(self.remaining_budget) + ' to spend until ' + str(self.end_date)

class User(AbstractUser):
    """User model for authentication"""

    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True, blank=False)
    budget     = models.ForeignKey(SpendingLimit, null = True, blank = True, on_delete=models.SET_NULL)

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
    budget = models.OneToOneField(SpendingLimit, null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

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