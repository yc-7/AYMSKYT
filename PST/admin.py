from django.contrib import admin
from .models import User, Category, Expenditure

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
<<<<<<< HEAD
        'title', 'price', 'category', 'date', 'description', 'receipt_image'
=======
        'id', 'user', 'category', 'title', 'price', 'date', 'description', 'receipt_image'
>>>>>>> 4bfb0187b2defa5cd7153ed108050b3cdcc80273
    ]