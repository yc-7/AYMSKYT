from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from minted.forms import TimeFrameForm
from minted.models import Category
from minted.views.views_functions.analytics_view_functions import generate_category_line_chart_dataset, generate_category_pie_chart_dataset, generate_all_spending_line_chart_dataset
import datetime

@login_required
def view_analytics(request):
    one_year_from_today = datetime.date.today() - datetime.timedelta(days=365)

    # Defaults
    start_date = one_year_from_today
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
    else:
        category_pie_chart_data = generate_category_pie_chart_dataset(categories, start_date, end_date)
        category_line_chart_data = generate_category_line_chart_dataset(categories, start_date, end_date, time_interval)
        all_spending_line_chart_data = generate_all_spending_line_chart_dataset(categories, start_date, end_date, time_interval)
        return render(request, 'analytics.html', {'form': form, 'category_pie_chart_data': category_pie_chart_data, 'category_line_chart_data': category_line_chart_data, 'all_spending_line_chart_data': all_spending_line_chart_data})
