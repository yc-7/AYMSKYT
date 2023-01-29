"""Models in the PST app"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager

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



TIMEFRAME = [
    ('/week', 'Weekly'),
    ('/month', 'Monthly'),
    ('/6 months', 'Half-yearly'),
    ('/year', 'Annually'),
    #('overall', 'Overall')
]

class SpendingLimit(models.Model):
    limit = models.DecimalField(default = None, max_digits = 12, decimal_places = 2, blank=False)
    timeframe = models.CharField(max_length=11, choices=TIMEFRAME, blank=False)



class Category(models.Model):
    """Model for expenditure categories"""

    user = models.ForeignKey(User, blank = False, on_delete= models.CASCADE)
    name = models.CharField(max_length = 50, blank = False)
    #budget = models.DecimalField(default = 0, max_digits = 6, decimal_places = 2)
    budget = models.OneToOneField(SpendingLimit, blank = True, on_delete=models.CASCADE)
