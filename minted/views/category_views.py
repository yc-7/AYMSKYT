from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from minted.forms import *
from minted.models import *
from minted.views.general_user_views.login_view_functions import *

class CategoryListView(LoginRequiredMixin, ListView):
    """View that displays a user's categories"""

    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in the template"""

        context = super().get_context_data(*args, **kwargs)
        current_user = self.request.user
        context['user'] = current_user
        context['categories'] = Category.objects.filter(user = current_user)
        return context

@login_required
def create_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        spending_form = SpendingLimitForm(request.POST)
        if category_form.is_valid() and spending_form.is_valid():
            spending = spending_form.save()
            category = category_form.save(commit=False)
            category.user = request.user
            category.budget = spending
            category.save()
            return redirect('category_list')           
    else:
        category_form = CategoryForm(initial={'user': request.user})
        spending_form = SpendingLimitForm()
    return render(request, 'create_category.html', {'category_form': category_form, 'spending_form': spending_form})

@login_required
def delete_category(request, category_id):
    if request.method == 'POST':
        if len(Category.objects.filter(id=category_id)) == 0:
            messages.add_message(request, messages.ERROR, "Category does not exist")
            return redirect('create_category')
        category = Category.objects.get(id=category_id)
        SpendingLimit.objects.get(category=category).delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted successfully")
    return redirect('category_list')

@login_required
def edit_category(request, category_id):
    if not category_id:
        return redirect('category_list')
    
    number_of_existing_categories = len(Category.objects.filter(id=category_id)) 
    
    if number_of_existing_categories == 0:
        messages.add_message(request, messages.ERROR, "Category does not exist")
        return redirect('create_category')

    category = Category.objects.get(id=category_id)
    spending = SpendingLimit.objects.get(category=category)

    if request.user != category.user and not request.user.is_superuser:
        return redirect('category_list')

    if request.method == 'POST':
        category_form = CategoryForm(instance=category, data=request.POST)
        spending_form = SpendingLimitForm(request.POST)
        if category_form.is_valid() and spending_form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            new_spending = spending_form.save()
            category = category_form.save(commit=False)
            category.budget = new_spending
            category.save()
            spending.delete()
            return redirect('category_list')
    else:
        category_form = CategoryForm(instance=category)
        spending_form = SpendingLimitForm(instance=spending)
    return render(request, 'edit_category.html', {'category_form': category_form, 'spending_form': spending_form, 'category_id': category.id})