from django import forms
from django.conf import settings
from django.shortcuts import redirect
from django.core.validators import RegexValidator

class LoginProhibitedMixin():
    """Mixin that redirects when a user is logged in"""

    def dispatch(self, *args, **kwargs):
        """Redirects when user is logged in, or dispatch otherwise"""

        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        """Handle when a user is already logged in"""

        url = self.get_redirect_url_when_logged_in()
        return redirect(url)

    def get_redirect_url_when_logged_in(self):
        """Return the url to redirect to when not logged in"""

        if self.request.user.is_staff:
            return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN
        else:
            return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER
        
class AdminProhibitedMixin():
    """Mixin that redirects when the user is an admin"""

    def dispatch(self, *args, **kwargs):
        """Redirects when user is an admin, or dispatch otherwise"""

        if self.request.user.is_staff:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN)
        return super().dispatch(*args, **kwargs)
        
class NewPasswordMixin(forms.Form):
    """Form mixin for new_password and password_confirmation fields"""

    new_password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators = [RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message = 'Password must contain an uppercase character, a lowercase character and a number'
            )]
    )
    password_confirmation = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors"""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Password does not match')
