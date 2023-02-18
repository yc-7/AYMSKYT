from django.shortcuts import redirect, render
from ..forms import *
from ..models import *
from .views_functions.login_view_functions import *
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')           
    else:
        form = CategoryForm(initial={'user': request.user})
    return render(request, 'create_category.html', {'form': form})


def delete_category(request, category_id):
    if request.method == 'POST':
        if len(Category.objects.filter(id=category_id)) == 0:
            messages.add_message(request, messages.ERROR, "Category does not exist")
            return redirect('create_category')
        Category.objects.get(id=category_id).delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted successfully")
    return redirect('category_list')


def category_list_view(request):
    current_user = request.user
    my_categories = Category.objects.filter(user = current_user)
    context = {'user': current_user,'categories': my_categories}
    return render(request, 'category_list.html', context)


def edit_category(request, category_id):
    if not category_id:
        return redirect('category_list')
    
    if len(Category.objects.filter(id=category_id)) == 0:
        messages.add_message(request, messages.ERROR, "Category does not exist")
        return redirect('create_category')

    category = Category.objects.get(id=category_id)

    if request.user != category.user and not request.user.is_superuser:
        return redirect('category_list')

    if request.method == 'POST':
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            print("here1")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category_id': category.id})