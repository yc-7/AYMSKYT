from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import FriendReqForm
from minted.models import User
from django.contrib import messages
from minted.views.friend_views.friend_view_functions import *
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

class NewFriendRequestView(LoginRequiredMixin, FormView):
    form_class = FriendReqForm
    template_name = 'friend_request.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        from_user = self.request.user

        recipient_does_not_exist = User.objects.filter(email=email).count() == 0
        if recipient_does_not_exist:
            messages.add_message(self.request, messages.ERROR, "User does not exist")
            return redirect('friend_request')

        to_user = User.objects.get(email=email)

        if not can_send_friend_request(from_user, to_user):
            messages.add_message(self.request, messages.ERROR, "You cannot send a friend request to this user!")
            return redirect('friend_request')

        FriendRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
        )
        if user_is_subscribed_to_friend_notifications(to_user):
            send_friend_request_notification(from_user, to_user)

        messages.add_message(self.request, messages.SUCCESS, "Friend request sent!")
        return redirect('profile')

class AcceptFriendRequestView(LoginRequiredMixin, View):
    """View that handles accepting friend requests"""
    http_method_name = ['post']

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

        if not to_user.notification_subscription:
            return redirect('request_list')

        if user_is_subscribed_to_friend_notifications(to_user):
            send_friend_request_accept_notification(to_user, from_user)

        return redirect('request_list')
    
class DeclineFriendRequestView(LoginRequiredMixin, View):
    """View that handles declining friend request"""
    http_method_name = ['post']

    def post(self, request, **kwargs):
        """Decline friend request"""
        friend_request_id = kwargs.get('friend_request_id')
        if not friend_request_id:
            return redirect('friend_list')
        
        friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request declined!")
        return redirect('request_list')

class FriendsListView(LoginRequiredMixin, ListView):
    """View that displays a users friends"""
    model = User
    template_name = 'friend_list.html'
    context_object_name = 'friends'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """Handle get request"""

        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return the user's friends"""

        current_user = self.request.user
        my_friends_list = current_user.friends.all()
        return my_friends_list

class FriendRequestListView(LoginRequiredMixin, ListView):
    """View to display a users incoming friend requests"""
    model = User
    template_name = 'request_list.html'
    context_object_name = 'requests'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """Handle get request"""
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return the user's friend requests"""
        current_user = self.request.user
        friend_requests_sent_to_current_user = FriendRequest.objects.filter(to_user = current_user)
        return friend_requests_sent_to_current_user

class UnfriendView(LoginRequiredMixin, View):
    """View that handles user unfriending"""
    http_method_name = ['post']

    def post(self, request, **kwargs):
        """Handle unfriend"""
        friend_id = kwargs.get('friend_id')
        if not friend_id:
            return redirect('friend_list')
        
        user_to_unfriend = get_object_or_404(User, id=friend_id)
        request.user.friends.remove(user_to_unfriend)
        user_to_unfriend.friends.remove(request.user)
        return redirect('friend_list')
    