from minted.decorators import staff_prohibited
from django.shortcuts import render
from minted.forms import TimeFrameForm
from minted.models import Category , Expenditure
from minted.views.analytics_views.analytics_view_functions import *
import datetime
from minted.views.budget_views_functions import *  

@staff_prohibited
def view_analytics(request):
    date_one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
    user = request.user

    # Defaults
    start_date = date_one_year_ago
    end_date = datetime.date.today()
    time_interval = 'monthly'
    budget = request.user.budget.budget
    form = TimeFrameForm(initial={
        'start_date': start_date, 
        'end_date': end_date, 
        'time_interval': time_interval})

    if request.method == 'POST':
        form = TimeFrameForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            time_interval = form.cleaned_data.get('time_interval')
    
    categories = Category.objects.filter(user = request.user)
    if not categories:
        return render(request, 'analytics.html', {'form': form})

    all_budgets = generate_budget_list(request.user, categories)
    colours = [category.colour for category in categories]
    category_pie_chart_data = generate_category_pie_chart_dataset(categories, start_date, end_date, float(budget))
    category_line_chart_data = generate_category_line_chart_dataset(categories, start_date, end_date, time_interval)
    overall_min_and_max_spending_categories = get_overall_max_and_min_spending_categories(category_pie_chart_data)
    categories_on_budget_percentage = calculate_categories_on_budget_percentage(user)
    percent_of_budget_remaining = calculate_percentage_of_budget_remaining(user)
    total_spending = calculate_total_spending(user)
    total_spending_between_dates = calculate_total_spending_between_dates(user, start_date, end_date)
    biggest_purchase = calculate_biggest_purchase(user)
    stats = {
        'extreme_labels':overall_min_and_max_spending_categories,
        'categories_on_budget_percentage': categories_on_budget_percentage,
        'percent_of_budget_remaining': percent_of_budget_remaining,
        'budget':all_budgets, 
        'total_spending': total_spending,
        'total_spending_between_dates': total_spending_between_dates,
        'biggest_purchase': biggest_purchase

    }

    return render(request, 'analytics.html', {
        'form': form, 
        'category_pie_chart_data': category_pie_chart_data, 
        'category_line_chart_data': category_line_chart_data, 
        'colours': colours, 'time_interval': time_interval, 
        'start_date':start_date, 
        'end_date':end_date,
        'stats': stats})

def dashboard_analytics(request):
    
    categories = Category.objects.filter(user = request.user)
    all_budgets = generate_budget_list(request.user, categories)
    user_budget = all_budgets[-1]

    start_date = user_budget.start_date
    end_date = user_budget.end_date
    budget = request.user.budget.budget
    
    transactions = Expenditure.objects.filter(category__user=request.user).order_by('-date')
    
    if not categories:
        return render(request, 'dashboard.html')
    

    spend_this_month_data = generate_all_spending_pie_chart_dataset(categories, start_date, end_date, float(budget))
    
    return render(request, 'dashboard.html', {'spend_this_month_data': spend_this_month_data, 'transactions': transactions})



    
