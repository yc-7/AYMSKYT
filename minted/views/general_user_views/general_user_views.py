from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import UpdateView
from minted.forms import *
from minted.models import *
from django.contrib import messages
from minted.decorators import login_prohibited
from minted.views.general_user_views.login_view_functions import *
from minted.views.general_user_views.point_system_views import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.conf import settings
from minted.decorators import login_prohibited
from minted.mixins import LoginProhibitedMixin
from minted.notifications import unsubscribe_user_from_push, is_user_subscribed
from minted.views.general_user_views.login_view_functions import *

class LogInView(LoginProhibitedMixin, View):
    """View that handles log in"""

    http_method_name = ['get', 'post']

    def get(self, request):
        """Display log in template"""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt"""

        form = LogInForm(request.POST)
        user = get_user(form)
        self.next = request.POST.get('next')
        if user is not None:
            login(request, user)
            self.next = request.POST.get('next') or get_redirect_url_for_user(user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "Log in credentials were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form"""

        form = LogInForm()
        return render(self.request, 'login.html', {'form': form, 'next': self.next})


def log_out(request):
    unsubscribe_user_from_push(request.user.id)
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'homepage.html')

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        spending_form = SpendingLimitForm(request.POST)
        if form.is_valid() and spending_form.is_valid():
            spending = spending_form.save()
            user = form.save(spending)
            update_streak(user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
        spending_form = SpendingLimitForm()
    return render(request, 'signup.html', {'form': form, 'spending_form': spending_form})

@login_required
def dashboard(request):
    return render(request,'dashboard.html')

@login_required
def profile(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user

    webpush_subscription_status = 'Subscribed' if is_user_subscribed(user.id) else 'Not subscribed'

    return render(request, 'profile.html', {'user': user, 'vapid_key': vapid_key, 'subscription_status': webpush_subscription_status})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """"View that handles updating a logged-in user's profile"""

    model = EditProfileForm
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

    def get_object(self):
        """Return the object (user) to be updated"""

        user = self.request.user
        return user

    def get_success_url(self):
        """Return the redirect URL after successful update"""

        messages.add_message(self.request, messages.SUCCESS, 'Profile updated')
        return reverse('profile')

@login_required
def edit_spending_limit(request):
    if request.method == 'POST':
        form = SpendingLimitForm(request.POST, instance=request.user.budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your spending limits were successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SpendingLimitForm(instance= request.user.budget)
    return render(request, 'edit_spending_limit.html', {'form': form})

@login_required
def change_password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('profile')
    form = PasswordForm()
    return render(request, 'change_password.html', {'form': form})
