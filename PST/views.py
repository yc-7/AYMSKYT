from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.contrib import messages
from .decorators import login_prohibited
from .views_functions import *

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            user = get_user(form)
            if user:
                login(request, user)
                redirect_url = request.POST.get('next') or get_redirect_url_for_user(user)
                return redirect(redirect_url)
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    next_url = request.GET.get('next') or ''
    return render(request, 'login.html', {'form': form, 'next': next_url})

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'home.html')


@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,'dashboard.html')
