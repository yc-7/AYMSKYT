from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from minted.views.budget_views_functions import *
from minted.mixins import AdminProhibitedMixin

def generate_budget_list(user, categories):
    all_budgets = []

    for category in categories:
        all_budgets.append(current_category_limit(category))
    if user.budget is not None:
        all_budgets.append(current_user_limit(user))

    return all_budgets

class BudgetListView(LoginRequiredMixin, AdminProhibitedMixin, ListView):
    """View that displays a user's budgets"""

    model = SpendingLimit
    template_name = 'budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        """Return the user's budgets"""

        current_user = self.request.user
        categories = current_user.get_categories()
        budgets = generate_budget_list(current_user, categories)
        return budgets
    
