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
    labels = []
    data = []
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()

    form = TimeFrameForm(initial={'start_date': start_date, 'end_date':end_date})

    if request.method == 'POST':
        form = TimeFrameForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
    

    categories = Category.objects.filter(user = request.user)
    print(categories)
    for category in categories:
        labels.append(category.name)
        data.append(int(category.get_total_expenses_for_category(dateFrom=start_date, dateTo=end_date)))
    
    # date = f"{start_date} - {end_date}"
    return render(request, 'analytics.html', {
        'form': form,
        'labels': labels,
        'data': data,
    })