from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from ..general_user_views.login_view_functions import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from minted.notifications import send_push
from minted.views.friend_views.friend_view_functions import *

@login_required
def friend_request(request):
    form = FriendReqForm(initial={'from_user':request.user, 'is_active': True})
    if request.method == 'POST':
        form = FriendReqForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            from_user = request.user
            is_active = form.cleaned_data.get('is_active')
            recipient_does_not_exist = User.objects.filter(email=email).count() == 0

            if recipient_does_not_exist:
                messages.add_message(request, messages.ERROR, "User does not exist")
                return redirect('friend_request') 
            
            recipient = User.objects.get(email=email)
            sent_to_self = (recipient == request.user)
            has_incoming_request = FriendRequest.objects.filter(from_user = recipient, to_user = request.user).count() != 0
            request_already_sent = FriendRequest.objects.filter(from_user = request.user, to_user = recipient).count() != 0
            

            if sent_to_self or request_already_sent or has_incoming_request:
                messages.add_message(request, messages.ERROR, "You cannot send a friend request to this user!")
                return redirect('friend_request') 
            
            to_user = User.objects.get(email = email)
            new_friend = FriendRequest.objects.create(
                from_user = from_user,
                to_user = to_user,
                is_active = True
            )
            if user_is_subscribed_to_friend_notifications(recipient):
                head = "You have received a friend request"
                body = f"{from_user} has send you a friend request"
                send_push(head, body, to_user.id)
        return redirect('profile') 
    
    return render(request, 'friend_request.html', {'form': form})

@login_required
def accept_request(request, friend_request_id):
    if request.method == 'POST':
        if FriendRequest.objects.filter(id = friend_request_id).count() == 0:
            messages.add_message(request, messages.ERROR, "Invalid request!")
            return redirect('request_list')


        friend_request = FriendRequest.objects.get(id = friend_request_id)

        from_user = friend_request.from_user
        to_user = friend_request.to_user

        make_friends(from_user, to_user)

        friend_request.is_active = False
        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request accepted!")

        if not to_user.notification_subscription:
            return redirect('request_list')

        if user_is_subscribed_to_friend_notifications(to_user):
            head = "Your friend request has been accepted!"
            body = f"You and {to_user.first_name} are now friends!"
            send_push(head, body, from_user.id)

        return redirect('request_list')

@login_required
def decline_request(request, friend_request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id = friend_request_id)
        friend_request.is_active = False
        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request declined!")
        return redirect('request_list')


@login_required
def friend_list_view(request):
    current_user = request.user
    my_friends_list = current_user.friends.all()
    context = {'user': current_user,'friends': my_friends_list}
    return render(request, 'friend_list.html', context)

@login_required
def request_list_view(request):
    current_user = request.user
    requests_sent_to_me_list = FriendRequest.objects.filter(to_user = current_user)
    context = {'user': current_user,'requests': requests_sent_to_me_list}
    return render(request, 'request_list.html', context)
                
@login_required
def unfriend_view(request,friend_id):
    if request.method == 'POST':
        user_to_unfriend = User.objects.get(id=friend_id)
        request.user.friends.remove(user_to_unfriend)
        user_to_unfriend.friends.remove(request.user)
        return redirect('friend_list')