from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from minted.mixins import AdminProhibitedMixin
from minted.forms import FriendReqForm
from minted.models import User
from minted.views.friend_views.friend_view_functions import *

class FriendsListView(AdminProhibitedMixin, LoginRequiredMixin, ListView):
    """View that displays a users friends"""
    
    model = User
    template_name = 'friends/friend_list.html'
    context_object_name = 'friends'
    http_method_names = ['get']
    paginate_by = settings.FRIENDS_PER_PAGE
    
    def get_queryset(self):
        """Return the user's friends"""

        current_user = self.request.user
        user_friends_list = current_user.friends.all().order_by('first_name')
        return user_friends_list

class NewFriendRequestView(AdminProhibitedMixin, LoginRequiredMixin, FormView):
    """View that handles sending friend requests"""

    form_class = FriendReqForm
    template_name = 'friends/friend_request.html'

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the friend request form"""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by making friend request"""

        email = form.cleaned_data.get('email')
        from_user = self.request.user
        to_user = User.objects.get(email = email)
        form.save()

        if user_is_subscribed_to_friend_notifications(to_user):
            send_friend_request_notification(from_user, to_user)

        messages.add_message(self.request, messages.SUCCESS, "Friend request sent!")
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return the redirect URL after successful friend request"""

        return reverse('friend_request')

class FriendRequestListView(AdminProhibitedMixin, LoginRequiredMixin, ListView):
    """View to display a users incoming friend requests"""
    model = User
    template_name = 'friends/request_list.html'
    context_object_name = 'requests'
    http_method_names = ['get']
    paginate_by = settings.REQUESTS_PER_PAGE
    
    def get_queryset(self):
        """Return the user's friend requests"""
        current_user = self.request.user
        friend_requests_sent_to_current_user = FriendRequest.objects.filter(to_user = current_user).order_by('from_user')
        return friend_requests_sent_to_current_user

class AcceptFriendRequestView(AdminProhibitedMixin, LoginRequiredMixin, View):
    """View that handles accepting friend requests"""
    http_method_name = ['get', 'post']

    def get(self, request, **kwargs):
        return redirect('request_list')

    def post(self, request, **kwargs):
        friend_request_id = kwargs.get('friend_request_id')
        user_has_no_friend_requests = FriendRequest.objects.filter(id = friend_request_id).count() == 0
        if user_has_no_friend_requests:
            messages.add_message(request, messages.ERROR, "Invalid request!")
            return redirect('request_list')

        friend_request = FriendRequest.objects.get(id = friend_request_id)

        from_user = friend_request.from_user
        to_user = friend_request.to_user

        make_friends(from_user, to_user)

        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request accepted!")

        if user_is_subscribed_to_friend_notifications(from_user):
            send_friend_request_accept_notification(to_user, from_user)

        return redirect('request_list')
    
class DeclineFriendRequestView(AdminProhibitedMixin, LoginRequiredMixin, View):
    """View that handles declining friend request"""
    http_method_name = ['get', 'post']

    def get(self, request, **kwargs):
        return redirect('request_list')

    def post(self, request, **kwargs):
        """Decline friend request"""
        friend_request_id = kwargs.get('friend_request_id')
        
        friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request declined!")
        return redirect('request_list')

class UnfriendView(AdminProhibitedMixin, LoginRequiredMixin, View):
    """View that handles user unfriending"""
    http_method_name = ['get', 'post']

    def get(self, request, **kwargs):
        return redirect('friend_list')

    def post(self, request, **kwargs):
        """Handle unfriend"""
        friend_id = kwargs.get('friend_id')
        
        user_to_unfriend = get_object_or_404(User, id=friend_id)
        request.user.friends.remove(user_to_unfriend)
        user_to_unfriend.friends.remove(request.user)
        return redirect('friend_list')
    