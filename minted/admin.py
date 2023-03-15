from django.contrib import admin
from .models import User, Category, Expenditure, Reward, SpendingLimit, Subscription, NotificationSubscription

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

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    readonly_fields = ['reward_id']
    list_display = [
        'brand_name', 'points_required', 'expiry_date', 'description', 'cover_image'
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