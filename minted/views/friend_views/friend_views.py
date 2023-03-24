from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import FriendReqForm
from minted.models import User
from django.contrib import messages
from minted.views.friend_views.friend_view_functions import *

@login_required
def friend_request(request):
    form = FriendReqForm(initial={'from_user':request.user})
    if request.method == 'POST':
        form = FriendReqForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            from_user = request.user
            recipient_does_not_exist = User.objects.filter(email=email).count() == 0

            if recipient_does_not_exist:
                messages.add_message(request, messages.ERROR, "User does not exist")
                return redirect('friend_request') 
            
            to_user = User.objects.get(email=email)
            
            if not can_send_friend_request(from_user, to_user):
                messages.add_message(request, messages.ERROR, "You cannot send a friend request to this user!")
                return redirect('friend_request') 

            FriendRequest.objects.create(
                from_user = from_user,
                to_user = to_user,
                is_active = True
            )
            if user_is_subscribed_to_friend_notifications(to_user):
                send_friend_request_notification(from_user, to_user)
        return redirect('profile') 
    
    return render(request, 'friend_request.html', {'form': form})

@login_required
def accept_request(request, friend_request_id):
    if request.method == 'POST':
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

@login_required
def decline_request(request, friend_request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id = friend_request_id)
        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request declined!")
        return redirect('request_list')


@login_required
def friend_list_view(request):
    current_user = request.user
    my_friends_list = current_user.friends.all()
    context = {'friends': my_friends_list}
    return render(request, 'friend_list.html', context)

@login_required
def request_list_view(request):
    current_user = request.user
    friend_requests_sent_to_current_user = FriendRequest.objects.filter(to_user = current_user)
    context = {'requests': friend_requests_sent_to_current_user}
    return render(request, 'request_list.html', context)
                
@login_required
def unfriend_view(request,friend_id):
    if request.method == 'POST':
        user_to_unfriend = User.objects.get(id=friend_id)
        request.user.friends.remove(user_to_unfriend)
        user_to_unfriend.friends.remove(request.user)
        return redirect('friend_list')
