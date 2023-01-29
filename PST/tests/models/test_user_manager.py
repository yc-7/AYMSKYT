from django.test import TestCase
from PST.models import User

class UserManagerModelTestCase(TestCase):
    """Unit tests for the UserManager"""

    def test_create_user(self):
        user = User.objects.create_user('johndoe@example.org', 'Password123')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(isinstance(user, User))

    def test_create_super_user(self):
        user = User.objects.create_superuser('janedoe@example.org', 'Password123')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(isinstance(user, User))
