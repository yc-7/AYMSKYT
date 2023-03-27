from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import decorators
from allauth.socialaccount.models import SocialAccount


def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            if SocialAccount.objects.filter(user=request.user.id).exists() and request.user.budget == None:
                return view_function(request)
            if request.user.is_staff:
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN)
            else:
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER)
        else:
            return view_function(request)
    return modified_view_function

def login_required(view_function):
    def modified_view_function(request, *args, **kw):
        if request.user.is_authenticated:
            if request.user.budget == None and request.user.is_staff == False:
                return redirect(settings.LOGIN_REDIRECT_URL)
        return view_function(request, *args, **kw)
    return decorators.login_required(modified_view_function)

def staff_prohibited(view_function):
    def modified_view_function(request, *args, **kw):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN)
        return view_function(request, *args, **kw)
    return login_required(modified_view_function)

def staff_required(view_function):
    def modified_view_function(request, *args, **kw):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER)
        return view_function(request, *args, **kw)
    return login_required(modified_view_function)
