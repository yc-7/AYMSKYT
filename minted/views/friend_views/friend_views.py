from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from minted.forms import FriendReqForm
from minted.models import User
from minted.views.friend_views.friend_view_functions import *

class FriendsListView(LoginRequiredMixin, ListView):
    """View that displays a users friends"""
    
    model = User
    template_name = 'friend_list.html'
    context_object_name = 'friends'
    http_method_names = ['get']
    
    def get_queryset(self):
        """Return the user's friends"""

        current_user = self.request.user
        my_friends_list = current_user.friends.all()
        return my_friends_list

class NewFriendRequestView(LoginRequiredMixin, FormView):
    """View that handles sending friend requests"""

    form_class = FriendReqForm
    template_name = 'friend_request.html'

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

class FriendRequestListView(LoginRequiredMixin, ListView):
    """View to display a users incoming friend requests"""
    model = User
    template_name = 'request_list.html'
    context_object_name = 'requests'
    http_method_names = ['get']
    
    def get_queryset(self):
        """Return the user's friend requests"""
        current_user = self.request.user
        friend_requests_sent_to_current_user = FriendRequest.objects.filter(to_user = current_user)
        return friend_requests_sent_to_current_user

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
    