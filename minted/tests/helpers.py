from unittest import TestCase
from django.urls import reverse

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
    
class LoginRequiredTester(TestCase):
    """Checks that users are redirected if they are not logged in"""

    def assertLoginRequired(self, url):
        redirect_url = redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 200)