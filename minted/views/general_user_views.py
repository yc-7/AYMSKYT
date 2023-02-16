from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from minted.forms import *
from minted.models import *
from django.contrib import messages
from minted.decorators import login_prohibited
from .views_functions.login_view_functions import *

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            user = get_user(form)
            if user:
                login(request, user)
                redirect_url = request.POST.get('next') or get_redirect_url_for_user(user)
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    return render(request, 'login.html', {'form': form, 'next': next_url})

def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'homepage.html')

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,'dashboard.html')


def category_expenditures(request, category_name):
    category = Category.objects.get(name=category_name)
    expenditures = Expenditure.objects.filter(category=category).order_by('-date')
    if request.method == 'POST':
        expenditure_id = int(request.POST['id'])
        expenditure = expenditures.get(id=expenditure_id)
        expenditure.delete()
        return redirect('expenditures', category_name=category_name)
    return render(request, 'expenditures/expenditures_list.html', { 'expenditures': expenditures, 'category': category })


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
                                'receipt_image': expenditure.receipt_image,
                              }
        form = ExpenditureForm(user=request.user, category=category_name, initial=current_expenditure)
    return render(request, 'expenditures/edit_expenditures.html', { 'form': form, 'expenditure': expenditure })

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
        
