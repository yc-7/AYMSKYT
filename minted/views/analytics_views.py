from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ..forms import *
from ..models import *
from django.contrib import messages
from ..decorators import login_prohibited
from .views_functions.login_view_functions import *
import random
import datetime


def view_analytics(request):
    pie_labels = []
    pie_data = []

    one_year_from_today = datetime.date.today() - datetime.timedelta(days=365)
    start_date = one_year_from_today
    end_date = datetime.date.today()

    form = TimeFrameForm(initial={'start_date': start_date, 'end_date': end_date})

    if request.method == 'POST':
        form = TimeFrameForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
    

    categories = Category.objects.filter(user = request.user)
    for category in categories:
        pie_labels.append(category.name)
        pie_data.append(int(category.get_total_expenses_for_category(date_from=start_date, date_to=end_date)))


    line_dataset = []
    all_dates = {}
    for category in categories:
        expenses_per_time = {}
        difference_in_days = end_date - start_date
        if difference_in_days.days > 1825:
            expenses = category.get_yearly_expenses_for_category(date_from= start_date, date_to=end_date)
        elif difference_in_days.days > 60:
            expenses = category.get_monthly_expenses_for_category(date_from=start_date, date_to=end_date)
        elif difference_in_days.days > 21:
            expenses = category.get_weekly_expenses_for_category(date_from=start_date, date_to=end_date)
        else:
            expenses = category.get_daily_expenses_for_category(date_from= start_date, date_to= end_date)
        for expense in expenses:
            if expense not in all_dates:
                all_dates[expense] = 0
            if expense not in expenses_per_time:
                expenses_per_time[expense] = 0
            expenses_per_time[expense] += expenses[expense]
        line_dataset.append({
            'category_name': category.name,
            'expenses_per_time': expenses_per_time
        })
    
    line_data = []
    for item in line_dataset:
        data=[]
        data_points = {
            'label': item['category_name'],
            'data': data,
            'fill': False,
            'borderColor': '',
            'backgroundColor': '',
            'pointHoverRadius': 8,
            'pointHoverBorderColor': 'white',
            'pointBorderColor': 'white',
            'pointStyle': 'rectRot',

        }
        for date, expense in item['expenses_per_time'].items():
            data.append({
                'x':date,
                'y':expense
            })
        line_data.append(data_points)
    
    
    chart_data = {
        'labels':list(all_dates.keys()), 
        'datasets': line_data
    }

    
    return render(request, 'analytics.html', {'form': form, 'pie_labels': pie_labels, 'pie_data': pie_data, 'chart_data': chart_data})
