from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from minted.views.budget_views_functions import get_budgets
from minted.mixins import AdminProhibitedMixin
from minted.forms import SpendingLimitForm
from minted.models import SpendingLimit

class BudgetListView(LoginRequiredMixin, AdminProhibitedMixin, ListView):
    """View that displays a user's budgets"""

    model = SpendingLimit
    template_name = 'budget_list.html'
    context_object_name = 'budgets'
    paginate_by = settings.BUDGETS_PER_PAGE

    def get_queryset(self):
        """Return the user's budgets"""

        current_user = self.request.user
        categories = current_user.get_categories()
        budgets = get_budgets(current_user, categories)
        return budgets

class EditSpendingLimitView(LoginRequiredMixin, AdminProhibitedMixin, UpdateView):
    """View that handles changing the user's overall budget"""

    form_class = SpendingLimitForm
    template_name = 'edit_spending_limit.html'

    def get_object(self):
        """Return the budget to be updated"""

        user = self.request.user
        budget = user.budget
        return budget
    
    def get_success_url(self):
        """Return the redirect URL after successful update"""

        messages.success(self.request, 'Your spending limits were successfully updated!')
        return reverse('profile')

