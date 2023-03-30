from minted.decorators import staff_prohibited
from django.shortcuts import render
from minted.forms import TimeFrameForm
from minted.models import Category
from minted.views.analytics_views.analytics_view_functions import *
import datetime

@staff_prohibited
def view_analytics(request):
    date_one_year_ago = datetime.date.today() - datetime.timedelta(days=365)

    # Defaults
    start_date = date_one_year_ago
    end_date = datetime.date.today()
    time_interval = 'monthly'
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

    colours = [category.colour for category in categories]
    category_pie_chart_data = generate_category_pie_chart_dataset(categories, start_date, end_date)
    category_line_chart_data = generate_category_line_chart_dataset(categories, start_date, end_date, time_interval)
    overall_min_and_max_spending_categories = get_overall_max_and_min_spending_categories(category_pie_chart_data)
    categories_on_budget_percentage = calculate_categories_on_budget_percentage(request)
    percent_of_budget_remaining = calculate_percentage_of_budget_remaining(request)

   
    
    
    return render(request, 'analytics.html', {
        'form': form, 
        'category_pie_chart_data': category_pie_chart_data, 
        'category_line_chart_data': category_line_chart_data, 
        'colours': colours, 'time_interval': time_interval, 
        'start_date':start_date, 'end_date':end_date, 
        'extreme_labels':overall_min_and_max_spending_categories,
        'categories_on_budget_percentage': categories_on_budget_percentage,
        'percent_of_budget_remaining': percent_of_budget_remaining})
