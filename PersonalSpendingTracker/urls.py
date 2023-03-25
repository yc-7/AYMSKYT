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
import os
from django.contrib import admin
from django.urls import include, path
from minted import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from minted.forms import NewPasswordForm

urlpatterns = [
    path('admin', admin.site.index, name='admin'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    path('accounts/', include('allauth.urls')),
    
    path("accounts/signup/", views.sign_up_part1, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('sign_up/', views.sign_up_part1, name='sign_up'),
    path('sign_up/account_details', views.sign_up_part2, name='sign_up_part2'),
    path('sign_up/spending/', views.spending_signup, name='spending_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/profile', views.edit_profile, name='edit_profile'),
    path('profile/edit/change_password/', views.change_password, name='change_password'),
    path('profile/', views.profile , name='profile'),

    path('analytics/', views.view_analytics, name='view_analytics'),

    path('category_list/<str:category_name>/', views.category_expenditures_view, name='category_expenditures'),
    path('category_list/<str:category_name>/edit_expenditure/<int:expenditure_id>/', views.edit_expenditure, name='edit_expenditure'),
    path('category_list/<str:category_name>/new_expenditure/', views.add_expenditure, name='add_expenditure'),
    path('category_list/<int:expenditure_id>/delete', views.delete_expenditure, name='delete_expenditure'),

    path('create_category/', views.create_category, name = 'create_category'),
    path('category/<int:category_id>/edit', views.edit_category, name ='edit_category'),
    path('category/<int:category_id>/delete', views.delete_category, name ='delete_category'),
    path('category_list/', views.category_list_view, name = 'category_list'),

    path('friend_request/', views.friend_request, name='friend_request'),
    path('friend_list/', views.friend_list_view, name='friend_list'),
    path('request_list/', views.request_list_view, name='request_list'),
    path('unfriend/<int:friend_id>', views.unfriend_view, name='unfriend'),
    path('accept_request/<int:friend_request_id>', views.accept_request, name='accept_request'),
    path('decline_request/<int:friend_request_id>', views.decline_request, name='decline_request'),
    
    path('profile/edit/spending_limit', views.edit_spending_limit, name='edit_spending_limit'),
    path('budget_list/', views.budget_list, name = 'budget_list'),

    path('rewards/', views.rewards_homepage, name='rewards'),
    path('rewards/<str:brand_name>/<str:reward_id>/', views.claim_reward, name='claim_reward'),
    path('rewards/my_rewards/', views.my_rewards, name='my_rewards'),
    path('rewards/<str:brand_name>/', views.filtered_rewards, name='filtered_rewards'),
    path('rewards/add', views.add_rewards, name='add_rewards'),
    path('rewards/admin', views.rewards_list, name='rewards_list'),
    path('rewards/<int:reward_id>/edit', views.edit_rewards, name='edit_rewards'),
    
    path('notification_subscription/create', views.create_notification_subscription, name='create_notification_subscription'),
    path('notification_subscription/edit', views.edit_notification_subscription, name='edit_notification_subscription'),
    
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        email_template_name="password_reset/password_reset_email.html", 
        template_name="password_reset/password_reset_form.html"
    ), name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset/password_reset_sent.html"
    ), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset/password_reset_confirm.html",
        form_class=NewPasswordForm,
    ), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset/password_reset_done.html"
    ), name="password_reset_complete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
