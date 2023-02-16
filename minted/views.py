from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .decorators import login_prohibited
from .views_functions import *
from minted.forms import SpendingLimitForm, LogInForm, SignUpForm, TestExpenditureForm
from minted.models import SpendingLimit, Category, User, Expenditure
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncQuarter

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            user = get_user(form)
            if user:
                login(request, user)
                # today = date.today()
                # if user.budget and user.budget.end_date < today:
                #     spending_limit = SpendingLimitForm({'budget': user.budget.budget, 'timeframe': user.budget.timeframe})
                #     if spending_limit.is_valid():
                #         user.budget = spending_limit.save()
                #         user.save()
                # categories = Category.objects.filter(user=user)
                # for category in categories:
                #     if category.budget and category.budget.end_date < today:
                #        category.budget = SpendingLimitForm(instance=ucategory.budget).save()
                #        category.save()
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
    user = request.user
    category = Category.objects.filter(user = user)[0]
    list = current_category_limit(category)
    return render(request,'dashboard.html', {'list': list})

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

def spending_limits_of_category(category):
    filtered_expenditures = Expenditure.objects.filter(category = category)
    timeframe = category.budget.timeframe
    budget = category.budget.budget
    if timeframe == '/week':
        return filtered_expenditures.annotate(week=TruncWeek('date')).values('week').annotate(remaining = budget - Sum('price')).order_by('week')
    if timeframe == '/month':
        return filtered_expenditures.annotate(month=TruncMonth('date')).values('month').annotate(remaining = budget - Sum('price')).order_by('month')
    if timeframe == '/quarter':
        return filtered_expenditures.annotate(quarter=TruncQuarter('date')).values('quarter').annotate(remaining = budget - Sum('price')).order_by('quarter')
    if timeframe == '/year':
        return filtered_expenditures.annotate(year=TruncYear('date')).values('year').annotate(remaining = budget - Sum('price')).order_by('year')

def current_category_limit(category):
    all_limits = spending_limits_of_category(category)
    timeframe = category.budget.timeframe
    budget = category.budget.budget
    today = date.today()
    if timeframe == '/week':
        end_date = today - timedelta(days=today.isocalendar().weekday) + relativedelta(days =+ 7)
        start_date = end_date - relativedelta(days =+ 6)
        for week in all_limits:
            if week['week'] == start_date:
                return 'You have a limit of £' + str(budget) + ' and have £' + str(week['remaining']) + ' remaining until ' + str(end_date)
    if timeframe == '/month':
        start_date = date(today.year, today.month, 1)
        end_date = date(today.year, (today.month+1)%12, 1) - timedelta(days=1)
        for month in all_limits:
            if month['month'] == start_date:
                return 'You have a limit of £' + str(budget) + ' and have £' + str(month['remaining']) + ' remaining until ' + str(end_date)
    if timeframe == '/quarter':
        quarter = (today.month-1)//3 + 1
        start_date = date(today.year, 3 * quarter - 2, 1)
        end_date = date(today.year, (3* quarter)%12 + 1, 1) + timedelta(days=-1)
        for quarter in all_limits:
            if quarter['quarter'] == start_date:
                return 'You have a limit of £' + str(budget) + ' and have £' + str(quarter['remaining']) + ' remaining until ' + str(end_date)
    if timeframe == '/year':
        start_date = date(today.year,1,1)
        end_date = date(today.year+1, 1, 1) - timedelta(days=1)
        for year in all_limits:
            if year['year'] == start_date:
                return 'You have a limit of £' + str(budget) + ' and have £' + str(year['remaining']) + ' remaining until ' + str(end_date)

