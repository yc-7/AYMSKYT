from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ..forms import *
from ..models import *
from django.contrib import messages
from ..decorators import login_prohibited
from .views_functions.login_view_functions import *
import datetime


def view_analytics(request):
    pie_labels = []
    pie_data = []
    line_data = []
    line_dataset = []

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

    for category in categories:
        expenses = category.get_monthly_expenses_for_category(date_from=start_date, date_to=end_date)
        monthly_expenses = {}
        for expense in expenses:
            month = expense
            if month not in monthly_expenses:
                monthly_expenses[month] = 0
            monthly_expenses[month] += expenses[expense]
        line_dataset.append({
            'category_name': category.name,
            'monthly_expenses': monthly_expenses
        })
    
    line_data = []
    for item in line_dataset:
        data = {
            'label': item['category_name'],
            'data': [],
            'fill': False,
        }
        for month, expense in item['monthly_expenses'].items():
            data['data'].append({
                'x':month,
                'y':expense
            })
        line_data.append(data)
    
    
    chart_data = {
        'labels':sorted(list(set(monthly_expenses.keys()))), 
        'datasets': line_data
    }
    


    
    return render(request, 'analytics.html', {'form': form, 'pie_labels': pie_labels, 'pie_data': pie_data, 'line_data': chart_data})
