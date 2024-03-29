from minted.views.budget_views.budget_views_functions import get_budgets
from minted.models import Category


def calculate_total_spending(user):
    expenditures = user.get_expenditures() 
    total_amount_spent = sum([expense.amount for expense in expenditures])
    return total_amount_spent

def calculate_total_spending_between_dates(user, start_date, end_date):
    categories = user.get_categories()
    total_amount_spent = 0
    for category in categories:
        expenditures = category.get_expenditures_between_dates(start_date, end_date) 
        total_amount_spent += sum([expense.amount for expense in expenditures])
    
    return total_amount_spent

def calculate_biggest_purchase(user):
    expenditures = user.get_expenditures() 
    expense_amounts = []
    if expenditures:
        for expense in expenditures:
            expense_amounts.append(expense.amount)
        max_value = max(expense_amounts)
        biggest_expense_index = [i for i in range(len(expense_amounts)) if expense_amounts[i] == max_value]
        biggest_expense_names = [expenditures[i].title for i in biggest_expense_index]
        expenses_dict = {'names': biggest_expense_names,
                        'amount': max_value}
        return expenses_dict

def calculate_categories_on_budget_percentage(user):
    categories = user.get_categories()
    all_budgets = get_budgets(user, categories)
    on_budget = []
    for budget in all_budgets[:-1]:
        if budget.spent <= budget.budget:
            on_budget.append(True)
        else:
            on_budget.append(False)
    count_true = sum(on_budget)
    percentage_of_on_budget = (count_true / len(all_budgets[:-1])) * 100
    return round(percentage_of_on_budget)

def calculate_percentage_of_budget_remaining(user):
    categories = Category.objects.filter(user = user)
    all_budgets = get_budgets(user, categories)
    overall_user_budget = all_budgets[-1]
    user_spent = float(overall_user_budget.spent)
    user_budget = float(overall_user_budget.budget)
    
    if user_spent <= user_budget:
        percentage_of_budget_remaining = ((user_budget - user_spent) / user_budget) * 100
    else:
        percentage_of_budget_remaining = 0
    return round(percentage_of_budget_remaining)

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

def generate_category_pie_chart_dataset(categories, start_date, end_date, budget):
    pie_labels = []
    pie_data = []
    total_spending = 0

    for category in categories:
        total_expenses_for_category = float(category.get_total_expenses_for_category(date_from=start_date, date_to=end_date))
        total_spending += total_expenses_for_category


        pie_labels.append(category.name)
        pie_data.append(total_expenses_for_category)
    
    
    category_pie_chart_data = {
        'labels': pie_labels,
        'data': pie_data
    }

    return category_pie_chart_data

def generate_all_spending_pie_chart_dataset(categories, start_date, end_date, budget):
    total_spending = 0

    for category in categories:
        total_expenses_for_category = float(category.get_total_expenses_for_category(date_from=start_date, date_to=end_date))
        total_spending += total_expenses_for_category

    remaining_budget = budget - total_spending

    remaining_budget = max(remaining_budget, 0)

    pie_labels = ['Total Spending', 'Remaining Budget']
    pie_data = [total_spending, remaining_budget]

    all_spending_pie_chart_data = {
        'labels': pie_labels,
        'data': pie_data,
    }

    return all_spending_pie_chart_data

def get_overall_max_and_min_spending_categories(category_pie_chart_data):
    pie_data = category_pie_chart_data['data']
    pie_labels = category_pie_chart_data['labels']

    min_value = min(pie_data)
    min_values = [i for i, value in enumerate(pie_data) if value == min_value] 
    min_labels = [pie_labels[i] for i in min_values] 
    extreme_labels_dict = {'min_labels': min_labels}  

    contains_expenditure = []
    for value in pie_data:
        if value > 0:
            contains_expenditure.append(True)
    if True in contains_expenditure:
        max_value = max(pie_data)
        max_values = [i for i, value in enumerate(pie_data) if value == max_value]
        max_labels = [pie_labels[i] for i in max_values] 
        extreme_labels_dict['max_labels']= max_labels 

    return extreme_labels_dict




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
