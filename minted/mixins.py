from django.conf import settings
from django.shortcuts import redirect

class LoginProhibitedMixin():
    """Mixin that redirects when a user is logged in"""

    def dispatch(self, *args, **kwargs):
        """Redirects when user is logged in, or dispatch otherwise"""

        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_url_when_logged_in()
        return redirect(url)

    def get_redirect_url_when_logged_in(self):
        """Return the url to redirect to when not logged in"""

        if self.request.user.is_staff:
            return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_ADMIN
        else:
            return settings.REDIRECT_URL_WHEN_LOGGED_IN_AS_USER
