from django.contrib import admin
<<<<<<< HEAD
from .models import User, Category, Expenditure, SpendingLimit, Streak
=======
from .models import User, Category, Expenditure, SpendingLimit, Subscription, NotificationSubscription
>>>>>>> a3442697934d430998adcbb33368adf5645ffb91

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'email', 'first_name', 'last_name', 'is_active', 'budget', 'notification_subscription'
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'name', 'budget'
    ]

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'category', 'title', 'amount', 'date', 'description', 'receipt'
    ]

@admin.register(SpendingLimit)
class SpendingLimitAdmin(admin.ModelAdmin):
    list_display = [
        'budget', 'timeframe'
    ]



@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = [
        'last_login_time', 'streak'
    ]
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'description'
    ]

@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'frequency'
    ]