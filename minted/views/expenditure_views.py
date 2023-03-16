from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from minted.views.expenditure_receipt_functions import handle_uploaded_file, delete_file
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def category_expenditures_view(request, category_name):
    category_exists = Category.objects.filter(user=request.user, name=category_name).count() != 0
    if not category_exists:
        return redirect('category_list')

    category = Category.objects.get(user=request.user, name=category_name)
    expenditures = Expenditure.objects.filter(category=category).order_by('-date')
    return render(request, 'expenditures/expenditures_list.html', { 'expenditures': expenditures, 'category': category })

@login_required
def delete_expenditure(request, expenditure_id):
    if request.method == 'POST':
        expenditure = Expenditure.objects.get(pk=expenditure_id)
        category = expenditure.category
        if request.user == category.user:
            if expenditure.receipt:
                delete_file(expenditure.receipt.path)
            expenditure.delete()
        return redirect('category_expenditures', category_name=category.name)
    return redirect('category_list')

@login_required
def edit_expenditure(request, category_name, expenditure_id):
    expenditure_exists = Expenditure.objects.filter(id=expenditure_id).count() != 0
    if not expenditure_exists:
        return redirect('category_list')
    
    expenditure = Expenditure.objects.get(id=expenditure_id)
    if request.user != expenditure.category.user:
        return redirect('category_list')

    form = ExpenditureForm(instance=expenditure)
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, instance=expenditure)
        if form.is_valid():
            expenditure = form.save(commit=False)
            new_file = request.FILES.get('receipt')
            # clear = request.POST.get('receipt-clear') # This is so broken
            current_receipt = expenditure.receipt
            update_file = new_file and current_receipt

            if update_file:
                delete_file(current_receipt.path)

            if new_file:
                receipt_path = handle_uploaded_file(new_file)
                expenditure.receipt = receipt_path

            expenditure.save()

            return redirect('category_expenditures', category_name=category_name)
    return render(request, 'expenditures/edit_expenditures.html', { 'form': form, 'expenditure': expenditure })


@login_required
def add_expenditure(request, category_name):
    if Category.objects.filter(user=request.user, name=category_name).exists() == False:
        return redirect('create_category')
    if request.method == 'POST':
        category = Category.objects.get(user=request.user, name=category_name) # Need to make sure there are no duplicate categories with same name
        form = ExpenditureForm(request.POST)
        if request.POST.get("addExpenditure"):
            if form.is_valid():
                expenditure = form.save(commit=False)
                file = request.FILES.get('receipt')
                expenditure.category = category

                if file:
                    receipt_path = handle_uploaded_file(file)
                    expenditure.receipt = receipt_path
                
                expenditure.save()

                return redirect('category_expenditures', category_name=category_name)
        elif request.POST.get("cancelAddition"):
            return redirect('category_expenditures', category_name=category_name)
    form = ExpenditureForm()
    return render(request, 'expenditures/add_expenditure.html', { 'form': form, 'category': category_name })
