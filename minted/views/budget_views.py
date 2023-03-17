from django.shortcuts import redirect, render
from minted.decorators import merged_decorator
from ..models import *
from django.contrib import messages
from .budget_views_functions import *

@merged_decorator
def budget_list(request):
    current_user = request.user
    categories = current_user.get_categories()
    all_budgets = []
    for category in categories:
        all_budgets.append(current_category_limit(category))
    all_budgets.append(current_user_limit(request.user))
    return render(request, 'budget_list.html', {'budget': all_budgets})