from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from minted.forms import *
from minted.models import *
from minted.decorators import login_prohibited, login_required, staff_prohibited
from minted.views.general_user_views.login_view_functions import *
from minted.views.general_user_views.point_system_views import *
from django.conf import settings
from minted.decorators import login_prohibited
from minted.mixins import LoginProhibitedMixin
from minted.notifications import unsubscribe_user_from_push, is_user_subscribed
from minted.views.general_user_views.login_view_functions import *
from minted.views.analytics_views.analytics_views import dashboard_analytics 

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
            update_streak(user)
            self.next = request.POST.get('next') or get_redirect_url_for_user(user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "Log in credentials were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form"""

        form = LogInForm()
        return render(self.request, 'account/login.html', {'form': form, 'next': self.next})

def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'homepage.html')

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            request.session['user_data'] = form.cleaned_data
            return redirect('budget_sign_up')
    else:
        form = SignUpForm()
    return render(request, 'account/sign_up.html', { 'form': form })

@login_prohibited
def budget_sign_up(request):
    user_data = request.session.get('user_data')
    if SocialAccount.objects.filter(user=request.user.id).exists() == False and user_data == None:
        return redirect('sign_up')
    if request.method == 'POST':
        form = SpendingLimitForm(request.POST)
        if 'cancel' in request.POST:
            if SocialAccount.objects.filter(user=request.user.id).exists():
                User.objects.get(email=request.user.email).delete()
            return redirect('sign_up')
        else:
            if form.is_valid():
                spending = form.save()
                if SocialAccount.objects.filter(user=request.user.id).exists():
                    user = request.user
                    user.budget = spending
                    user.streak_data = Streak.objects.create()
                    user.save()
                    update_streak(user)
                else:
                    user = SignUpForm(user_data=user_data).save(spending)
                    update_streak(user)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                redirect_url = request.POST.get('next') or get_redirect_url_for_user(user)
                return redirect(redirect_url)
    else:
        form = SpendingLimitForm()
    return render(request, 'account/budget_sign_up.html', { 'form': form })

@staff_prohibited
def dashboard(request):
    if SocialAccount.objects.filter(user=request.user.id).exists():
            update_streak(request.user)
    return dashboard_analytics(request)

@staff_prohibited
def help_page(request):
    return render(request, 'help_page.html')

@login_required
def profile(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user

    webpush_subscription_status = 'On' if is_user_subscribed(user.id) else 'Off'

    return render(request, 'profile.html', {'user': user, 'vapid_key': vapid_key, 'subscription_status': webpush_subscription_status})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """"View that handles updating a logged-in user's profile"""

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

@staff_prohibited
def edit_spending_limit(request):
    if request.method == 'POST':
        if request.user.budget is not None:
            form = SpendingLimitForm(request.POST, instance=request.user.budget)
        else:
            form = SpendingLimitForm(request.POST)
        if form.is_valid():
            new_spending = form.save()
            request.user.budget = new_spending
            request.user.save()
            messages.success(request, 'Your spending limits were successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        if request.user.budget is not None:
            form = SpendingLimitForm(instance= request.user.budget)
        else:
            form = SpendingLimitForm()
    return render(request, 'edit_spending_limit.html', {'form': form})

class PasswordView(LoginRequiredMixin, FormView):
    """View that handles password change requests"""

    template_name = 'change_password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password form"""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        """Redirect if a user is signed in with google"""

        if SocialAccount.objects.filter(user = self.request.user.id).exists():
            messages.add_message(self.request, messages.ERROR, 'You are signed in with a Google Account')
            return redirect('profile')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Handle valid form by saving the new password"""

        form.save()
        login(self.request, self.request.user, backend = 'django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

    def get_success_url(self):
        """Return the redirect URL after successful password change"""

        messages.add_message(self.request, messages.SUCCESS, 'Password updated')
        return reverse('profile')
