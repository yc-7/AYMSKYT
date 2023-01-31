from django.shortcuts import redirect
from django.conf import settings

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
