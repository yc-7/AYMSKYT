from django.test import TestCase
from django.urls import reverse
from minted.models import  User
from minted.tests.helpers import LoginRequiredTester

class PointsLeaderboardViewTestCase(TestCase, LoginRequiredTester):
    """Unit tests for the points leaderboard view"""

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        'minted/tests/fixtures/default_spending_limit.json'
    ]

    def setUp(self):
        self.url = reverse('points_leaderboard')
        self.user = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)

        self.user.friends.add(self.other_user)

    def test_points_leaderboard_url(self):
        self.assertEqual(self.url,"/leaderboard/points")

    def test_view_redirects_to_login_if_not_logged_in(self):
        self.assertLoginRequired(self.url)

    def test_get_points_leaderboard(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboards/points_leaderboard.html')

    def test_get_points_leaderboard_has_correct_users_displayed(self):
        self.client.login(email = self.user.email, password = 'Password123')
        response = self.client.get(self.url)
        users = response.context['users']

        self.assertIn(self.user, users)
        self.assertIn(self.other_user, users)

        self._check_points_in_correct_order(users)

    def test_get_points_leaderboard_only_displays_self_if_no_friends(self):
        self.client.login(email = self.user.email, password = 'Password123')
        self.user.friends.clear()
        response = self.client.get(self.url)
        users = response.context['users']

        self.assertIn(self.user, users)
        self.assertNotIn(self.other_user, users)
        
        self._check_points_in_correct_order(users)
    
    def _check_points_in_correct_order(self, users):
        previous = float("inf")
        for user in users:
            self.assertGreaterEqual(previous, user.points)
            previous = user.points