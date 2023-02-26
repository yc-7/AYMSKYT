from django.test import TestCase
from minted.models import User, SpendingLimit

class UserManagerModelTestCase(TestCase):
    """Unit tests for the UserManager"""

    fixtures = [
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.user_limits = SpendingLimit.objects.get(pk=1)

    def test_create_user(self):
        user = User.objects.create_user('johndoe@example.org', 'Password123', budget=self.user_limits)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(isinstance(user, User))

    def test_create_super_user(self):
        user = User.objects.create_superuser('janedoe@example.org', 'Password123', budget=self.user_limits)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(isinstance(user, User))
