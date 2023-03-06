from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages


@login_required
def rewards_homepage(request):
    return render(request, 'rewards/rewards_home.html')

