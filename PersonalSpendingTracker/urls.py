"""PersonalSpendingTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from minted import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.view_analytics, name='view_analytics'),
    path('category_list/<str:category_name>/', views.category_expenditures, name='expenditures'),
    path('category_list/<str:category_name>/edit_expenditure/<int:expenditure_id>/', views.edit_expenditure, name='edit_expenditure'),
    path('category_list/<str:category_name>/new_expenditure/', views.add_expenditure, name='add_expenditure'),
    path('create_category/', views.create_category, name = 'create_category'),
    path('category/<int:category_id>/edit', views.edit_category, name ='edit_category'),
    path('category/<int:category_id>/delete', views.delete_category, name ='delete_category'),
    path('category_list/', views.category_list_view, name = 'category_list'),
    path('profile/', views.profile , name='profile'),
    path('profile/edit/profile', views.edit_profile, name='edit_profile'),
    path('profile/edit/spending_limit', views.edit_spending_limit, name='edit_spending_limit'),
    path('profile/edit/change_password/', views.change_password, name='change_password'),
    path('budget_list/', views.budget_list, name = 'budget_list'),

]
