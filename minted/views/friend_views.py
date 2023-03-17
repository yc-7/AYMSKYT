from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages
from django.core.exceptions import ValidationError

@login_required
def friend_request(request):
    form = FriendReqForm(initial={'from_user':request.user, 'is_active': True})
    if request.method == 'POST':
        form = FriendReqForm(request.POST)
        if form.is_valid():
              email = form.cleaned_data.get('email')
              from_user = request.user
              is_active = form.cleaned_data.get('is_active')

              if User.objects.filter(email=email).count() == 0 or (User.objects.get(email=email) == request.user):
                return redirect('friend_request') 
              
              user = User.objects.get(email = email)
              new_friend = FriendRequest.objects.create(
                from_user = from_user,
                to_user = user,
                is_active = True)
        new_friend.save()
        return redirect('profile') 
    return render(request, 'friend_request.html', {'form': form})

@login_required
def accept_request(request, request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id = request_id)
        #add who sent the request to the recipient's friend list
        friend_request.to_user.friends.add(friend_request.from_user)
        #add the recipient to the sender's friend list
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.is_active = False
        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request accepted!")
        return redirect('request_list')

@login_required
def decline_request(request, request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id = request_id)
        friend_request.is_active = False
        friend_request.delete()
        messages.add_message(request, messages.SUCCESS, "Friend request declined!")
        return redirect('request_list')


@login_required
def friend_list_view(request):
    current_user = request.user
    my_friends_list = User.objects.filter(current_user.friends)
    context = {'user': current_user,'friends': my_friends_list}
    return render(request, 'friend_list.html', context)

@login_required
def request_list_view(request):
    current_user = request.user
    requests_sent_to_me_list = FriendRequest.objects.filter(to_user = current_user)
    context = {'user': current_user,'requests': requests_sent_to_me_list}
    return render(request, 'request_list.html', context)
                

    