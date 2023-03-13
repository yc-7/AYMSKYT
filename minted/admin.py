from django.contrib import admin
from .models import User, Category, Expenditure, SpendingLimit, Streak

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'email', 'first_name', 'last_name', 'is_active', 'budget'
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