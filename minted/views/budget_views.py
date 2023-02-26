from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib import messages
from .budget_views_functions import *
    
@login_required
def budget_list(request):
    current_user = request.user
    categories = Category.objects.filter(user = current_user)
    all_budgets = []
    for category in categories:
        all_budgets.append(current_category_limit(category))
    all_budgets.append(current_user_limit(request.user))
    return render(request, 'budget_list.html', {'budget': all_budgets})