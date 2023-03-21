from django.shortcuts import redirect, render
from minted.decorators import staff_prohibited
from minted.forms import *
from minted.models import *
from minted.views.general_user_views.login_view_functions import *
from django.contrib import messages

@staff_prohibited
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