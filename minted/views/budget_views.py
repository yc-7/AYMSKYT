from django.shortcuts import render
from minted.decorators import staff_prohibited
from ..models import *
from django.contrib import messages
from .budget_views_functions import *
    

def generate_budget_list(user, categories):
    all_budgets = []

    for category in categories:
        all_budgets.append(current_category_limit(category))
    if user.budget is not None:
        all_budgets.append(current_user_limit(user))

    return all_budgets

@staff_prohibited
def budget_list(request):
    current_user = request.user
    categories = current_user.get_categories()

    all_budgets = generate_budget_list(current_user, categories)

    return render(request, 'budget_list.html', {'budget': all_budgets})


    


