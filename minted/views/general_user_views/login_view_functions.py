from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
import urllib

def get_user(form):
    """Returns authenticated user if possible"""

    user = None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email = email, password = password)
    return user

def get_redirect_url_for_user(user):
    """Returns redirect url for user based on user role"""

    if user.is_staff and user.is_superuser:
        return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN
    return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER

def redirect_with_queries(url, **queries):
    """A regular html redirect but with optional added queries"""

    response = redirect(url)
    if queries:
        query_string = urllib.parse.urlencode(queries)
        response['location'] += '?' + query_string
    return response