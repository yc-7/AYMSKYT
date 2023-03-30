from minted.views.budget_views import generate_budget_list
from minted.models import *

def calculate_categories_on_budget_percentage(request):
    user = request.user
    categories = Category.objects.filter(user = user)
    all_budgets = generate_budget_list(user, categories)
    on_budget = []
    for budget in all_budgets[:-1]:
        if budget.spent <= budget.budget:
            on_budget.append(True)
        else:
            on_budget.append(False)
    count_true = sum(on_budget)
    percentage_of_on_budget = (count_true / len(all_budgets[:-1])) * 100
    return percentage_of_on_budget

def calculate_percentage_of_budget_remaining(request):
    user = request.user
    categories = Category.objects.filter(user = user)
    all_budgets = generate_budget_list(user, categories)
    overall_user_budget = all_budgets[-1]
    user_spent = float(overall_user_budget.spent)
    user_budget = float(overall_user_budget.budget)
    
    if user_spent <= user_budget:
        percentage_of_budget_remaining = ((user_budget - user_spent) / user_budget) * 100
    else:
        percentage_of_budget_remaining = 0
    return percentage_of_budget_remaining

def get_category_expenses_for_time_interval(category, time_interval, start_date, end_date):
    if time_interval == 'yearly':
        expenses = category.get_yearly_expenses_for_category(date_from = start_date, date_to = end_date)
    elif time_interval == 'monthly':
        expenses = category.get_monthly_expenses_for_category(date_from = start_date, date_to = end_date)
    elif time_interval == 'weekly':
        expenses = category.get_weekly_expenses_for_category(date_from = start_date, date_to = end_date)
    else:
        expenses = category.get_daily_expenses_for_category(date_from = start_date, date_to = end_date)
    
    return expenses

def create_labels(categories, time_interval, start_date, end_date):
    labels = []
    if categories:
        labels = list(get_category_expenses_for_time_interval(categories[0], time_interval, start_date, end_date).keys())

    return labels

def create_data(expenses):
    data = []
    for date, expense in expenses:
        data.append({
            'x': date, 
            'y': expense
        })
    return data

def create_line_dataset(categories, time_interval, start_date, end_date):
    line_dataset = []
    for category in categories:
        
        expenses = get_category_expenses_for_time_interval(category, time_interval, start_date, end_date)

        line_dataset.append({
            'category_name': category.name,
            'expenses_per_time': expenses
        })
    return line_dataset

def generate_category_pie_chart_dataset(categories, start_date, end_date):
    pie_labels = []
    pie_data = []

    for category in categories:
        total_expenses_for_category = float(category.get_total_expenses_for_category(date_from=start_date, date_to=end_date))

        pie_labels.append(category.name)
        pie_data.append(total_expenses_for_category)
    
    category_pie_chart_data = {
        'labels': pie_labels,
        'data': pie_data
    }

    return category_pie_chart_data

def get_overall_max_and_min_spending_categories(category_pie_chart_data):
    pie_data = category_pie_chart_data['data']
    pie_labels = category_pie_chart_data['labels']

    max_value = max(pie_data)
    min_value = min(pie_data)

    max_values = [i for i, value in enumerate(pie_data) if value == max_value]
    min_values = [i for i, value in enumerate(pie_data) if value == min_value] 

    max_labels = [pie_labels[i] for i in max_values]
    min_labels = [pie_labels[i] for i in min_values]       

    return {'max_labels': max_labels, 'min_labels': min_labels}




def generate_category_line_chart_dataset(categories, start_date, end_date, time_interval):
    labels = create_labels(categories,time_interval, start_date, end_date)

    line_dataset = create_line_dataset(categories, time_interval, start_date, end_date)

    all_expenses = {}

    for item in line_dataset:
        for date, expense in item['expenses_per_time'].items():
            all_expenses[date] = all_expenses.get(date, 0) + expense
    
    line_dataset.append({
        'category_name': 'Total spending',
        'expenses_per_time': all_expenses})
    
    line_data = []
    for item in line_dataset:
        data = create_data(item['expenses_per_time'].items())
        
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
        
        line_data.append(data_points)
    
    category_line_chart_data = {
        'labels': labels,
        'datasets': line_data
    }

    return category_line_chart_data
