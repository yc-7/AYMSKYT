from django.shortcuts import redirect, render
from minted.decorators import staff_prohibited, login_required
from minted.forms import *
from minted.models import *
from minted.views.general_user_views.login_view_functions import *
from django.contrib import messages
from minted.views.category_views.category_view_functions import *

@staff_prohibited
def create_category(request):
    category_form = CategoryForm(user=request.user)
    spending_form = SpendingLimitForm()

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, user=request.user)
        spending_form = SpendingLimitForm(request.POST)
        if category_form.is_valid() and spending_form.is_valid():
            create_category_from_forms(request.user, category_form, spending_form, request.POST.get('colour_value', ""))
            return redirect('category_list')           
    return render(request, 'create_category.html', {'category_form': category_form, 'spending_form': spending_form})

@staff_prohibited
def delete_category(request, category_id):
    if request.method == 'POST':
        if len(Category.objects.filter(id=category_id)) == 0:
            messages.add_message(request, messages.ERROR, "Category does not exist")
            return redirect('create_category')
        category = Category.objects.get(id=category_id)
        SpendingLimit.objects.get(category=category).delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted successfully")
    return redirect('category_list')

@staff_prohibited
def category_list_view(request):
    current_user = request.user
    my_categories = Category.objects.filter(user = current_user)
    context = {'user': current_user,'categories': my_categories}
    return render(request, 'category_list.html', context)

@staff_prohibited
def edit_category(request, category_id):
    if not category_id:
        return redirect('category_list')
    
    number_of_existing_categories = len(Category.objects.filter(id=category_id)) 
    
    if number_of_existing_categories == 0:
        messages.add_message(request, messages.ERROR, "Category does not exist")
        return redirect('create_category')

    category = Category.objects.get(id=category_id)
    spending_limit = SpendingLimit.objects.get(category=category)

    if request.user != category.user and not request.user.is_superuser:
        return redirect('category_list')

    category_form = CategoryForm(instance=category)
    spending_form = SpendingLimitForm(instance=spending_limit)
    category_colour = ""
    category = Category.objects.get(pk=category_id)
    if category.colour:
        category_colour = category.colour

    if request.method == 'POST':
        category_form = CategoryForm(instance=category, data=request.POST)
        spending_form = SpendingLimitForm(request.POST)
        if category_form.is_valid() and spending_form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            edit_category_from_forms(category_form, spending_form, spending_limit, request.POST.get('colour_value', ""))
            return redirect('category_list')
    
    context = {'category_form': category_form, 'spending_form': spending_form, 'category_id': category.id, 'category_colour': category_colour}
    return render(request, 'edit_category.html', context)
