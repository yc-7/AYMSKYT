from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib import messages
from .budget_views_functions import *
from minted.views.general_user_views.point_system_view_function import all_budgets
    
@login_required
def budget_list(request):
    current_user = request.user
    categories = current_user.get_categories()

    if len(all_budgets) != 0:
        all_budgets.clear()

    for category in categories:
        all_budgets.append(current_category_limit(category))
    all_budgets.append(current_user_limit(request.user))

    return render(request, 'budget_list.html', {'budget': all_budgets})


    


