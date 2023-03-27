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
    def assertLoginRequired(self, url):
        response = self.client.get(url)
        login_url_name = 'log_in'
        self.assertRedirects(response, reverse_with_next(login_url_name, url))