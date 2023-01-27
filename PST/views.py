from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.

def login_prohibitied(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('#####ADMIN PAGE DOESNT EXIST####', user_id=request.user.id)
            else:
                return redirect('dashboard', user_id=request.user.id)
        else:
            return view_function(request)
    return modified_view_function

#login page for clients (admins use /admin/)

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data.get('email'))
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
                form = LogInForm()
                return render(request, 'login.html', {'form': form})
            else:
                username = user.username
                password = form.cleaned_data.get('password')
                login(request, user)
                if user.is_staff:
                    return redirect('#####ADMIN PAGE DOESNT EXIST####', user_id=user.id)
                else:
                    return redirect('dashboard', user_id=user.id)
    else:
        form = LogInForm()
        return render(request, 'login.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

#home page

def home(request):
    return render(request, 'home.html')

#signup page, redirects to login once account has been created
@login_prohibitied
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
def dashboard(request, user_id):
    return render(request,'dashboard.html', {'user_id': user_id})
