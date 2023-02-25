from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
import urllib

def get_user(form):
    """Autheticates user from login form
    Parameters
    ---
    form
        login form

    Returns
    ---
    User
        User object
    None 
        if credentials are invalid
    """
    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password')
    return authenticate(email=email, password=password)

def get_redirect_url_for_user(user):
    """ get url for user based on user role

    Parameters
    ---
    user
        User object
    
    Returns
    ---
    url
        redirect url for user
    """
    if user.is_staff and user.is_superuser:
        return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN
    return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER

def redirect_with_queries(url, **queries):
    """
    A regular html redirect but with optional added queries
    """

    response = redirect(url)
    if queries:
        query_string = urllib.parse.urlencode(queries)
        response['location'] += '?' + query_string
    return response