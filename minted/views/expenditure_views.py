from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages

@login_required
def category_expenditures(request, category_name):
    category = Category.objects.get(user=request.user, name=category_name)
    expenditures = Expenditure.objects.filter(category=category).order_by('-date')
    if request.method == 'POST':
        expenditure_id = int(request.POST['id'])
        expenditure = expenditures.get(id=expenditure_id)
        expenditure.delete()
        return redirect('expenditures', category_name=category_name)
    return render(request, 'expenditures/expenditures_list.html', { 'expenditures': expenditures, 'category': category })

@login_required
def edit_expenditure(request, category_name, expenditure_id):
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, user=request.user, category=category_name)
        if form.is_valid():
            form.update(expenditure_id)
            return redirect('expenditures', category_name=category_name)
    else:
        expenditure = Expenditure.objects.get(id=expenditure_id)
        current_expenditure = { 'title': expenditure.title,
                                'price': expenditure.price,
                                'date': expenditure.date,
                                'description': expenditure.description,
                                'receipt': expenditure.receipt,
                              }
        form = ExpenditureForm(user=request.user, category=category_name, initial=current_expenditure)
    return render(request, 'expenditures/edit_expenditures.html', { 'form': form, 'expenditure': expenditure })

@login_required
def add_expenditure(request, category_name):
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, user=request.user, category=category_name)
        if request.POST.get("addExpenditure"):
            if form.is_valid():
                form.save()
                return redirect('expenditures', category_name=category_name)
        elif request.POST.get("cancelAddition"):
            return redirect('expenditures', category_name=category_name)
    form = ExpenditureForm(user=request.user, category=category_name)
    return render(request, 'expenditures/add_expenditure.html', { 'form': form, 'category': category_name })