from django.contrib import admin
from .models import User, Category, Expenditure, SpendingLimit

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'email', 'first_name', 'last_name', 'is_active'
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'name', 'budget'
    ]

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'category', 'title', 'price', 'date', 'description', 'receipt_image'
    ]

@admin.register(SpendingLimit)
class SpendingLimitAdmin(admin.ModelAdmin):
    list_display = [
        'budget', 'timeframe'
    ]