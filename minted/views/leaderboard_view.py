from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from minted.models import User

class LeaderboardView(LoginRequiredMixin, ListView):
    """View that displays the leaderboard"""

    model = User
    template_name = 'leaderboard.html'
    context_object_name = 'users'

    def get_queryset(self):
        """"""

        users = User.objects.all().order_by('-streak_data')
        return users

        


