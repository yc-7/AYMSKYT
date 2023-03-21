from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN)
            else:
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER)
        else:
            return view_function(request)
    return modified_view_function

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