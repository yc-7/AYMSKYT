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
from django.urls import include, path
from minted import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('log_in/', views.LogInView.as_view(), name = 'log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/profile', views.edit_profile, name='edit_profile'),
    path('profile/edit/change_password/', views.change_password, name='change_password'),
    path('profile/', views.profile , name='profile'),

    path('analytics/', views.view_analytics, name='view_analytics'),

    path('category_list/<str:category_name>/', views.category_expenditures_view, name='category_expenditures'),
    path('category_list/<str:category_name>/edit_expenditure/<int:expenditure_id>/', views.edit_expenditure, name='edit_expenditure'),
    path('category_list/<str:category_name>/new_expenditure/', views.add_expenditure, name='add_expenditure'),
    path('category_list/<int:expenditure_id>/delete', views.delete_expenditure, name='delete_expenditure'),

    path('category_list/', views.CategoryListView.as_view(), name = 'category_list'),
    path('create_category/', views.create_category, name = 'create_category'),
    path('category/<int:category_id>/edit', views.edit_category, name ='edit_category'),
    path('category/<int:category_id>/delete', views.delete_category, name ='delete_category'),
    
    path('profile/edit/spending_limit', views.edit_spending_limit, name='edit_spending_limit'),
    path('budget_list/', views.budget_list, name = 'budget_list'),

    path('notification_subscription/create', views.create_notification_subscription, name='create_notification_subscription'),
    path('notification_subscription/edit', views.edit_notification_subscription, name='edit_notification_subscription'),
    
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)