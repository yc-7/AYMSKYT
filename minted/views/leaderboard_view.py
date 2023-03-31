from django.contrib.auth.mixins import LoginRequiredMixin
from minted.mixins import AdminProhibitedMixin
from django.views.generic import ListView
from minted.models import User

class LeaderboardView(AdminProhibitedMixin, LoginRequiredMixin, ListView):
    """View that displays the leaderboard"""

    model = User
    context_object_name = 'users'

    def get_queryset(self):
        """Return"""

        current_user = self.request.user
        friends = list(current_user.friends.all()) + [current_user]
        return friends
    
class PointsLeaderboardView(LeaderboardView):

    template_name = 'leaderboards/points_leaderboard.html'
    
    def get_queryset(self):
        friends = super().get_queryset()
        friends.sort(reverse = True, key = self.getPoints)
        return friends
    
    def getPoints(self, user):
        """Return a user's points"""

        return user.points
    
class StreaksLeaderboardView(LeaderboardView):

    template_name = 'leaderboards/streaks_leaderboard.html'
    
    def get_queryset(self):
        friends = super().get_queryset()
        friends.sort(reverse = True, key = self.getStreaks)
        return friends
    
    def getStreaks(self, user):
        """Return a user's streaks"""

        return user.streak_data.streak
        
