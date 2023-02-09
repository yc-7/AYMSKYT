from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .decorators import login_prohibited
from .views_functions import *
from minted.forms import SpendingLimitForm, LogInForm, SignUpForm, TestExpenditureForm
from minted.models import SpendingLimit, Category, User, Expenditure

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

def test_category(request):
    categories = Category.objects.all()
    return render(request, 'test_category.html', {'categories': categories})

def calculate(self, expenditure, timeframe):
    year = expenditure.date.isocalendar().year
    week = expenditure.date.isocalendar().week
    month = expenditure.month
    quarter = (month-1)/3 + 1

    filter_by_year = Expenditure.objects.filter(pub_date__year=year)

    if (timeframe.equals('month')):
        filter_by_year.filter(pub_date__month=month)
    if (timeframe.equals('week')):
        filter_by_year.filter(pub_date__week=week)
    if (timeframe.equals('quarter')):
        filter_by_year.filter(pub_date__quarter=quarter)
    return filter_by_year

def test_spending(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        return redirect('category')
    else:
        if request.method == 'POST':
            form = SpendingLimitForm(request.POST)
            if form.is_valid():
                spending_limit = form.save()
                budget = spending_limit.remaining_budget
                for i in Expenditure.objects.all():
                    if i.date >= spending_limit.start_date and i.date <= spending_limit.end_date:
                        budget = budget - i.price
                spending_limit.remaining_budget = budget
                spending_limit.save()
                category.budget = spending_limit
                category.save()
        else:
            form = SpendingLimitForm()
    return render(request, 'test_spending.html', {'form': form, 'category_id': category_id})

def test_expenditure(request):
    if request.method == 'POST':
        form = TestExpenditureForm(request.POST)
        if form.is_valid():
            expenditure = form.save()
            if expenditure.category.budget:
                if (expenditure.category.budget.start_date <= expenditure.date and expenditure.category.budget.end_date >= expenditure.date):
                    expenditure.category.budget.remaining_budget -= expenditure.price
                    expenditure.category.budget.save()
    else:
        form = TestExpenditureForm()
    return render(request, 'test_expenditure.html', {'form': form})
