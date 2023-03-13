from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages
from django.core.exceptions import ValidationError

def friend_request(request):
    form = FriendReqForm(initial={'from_user':request.user, 'is_active': True})
    if request.method == 'POST':
        form = FriendReqForm(request.POST)
        if form.is_valid():
              email = form.cleaned_data.get('email')
              from_user = request.user
              is_active = form.cleaned_data.get('is_active')
              if User.objects.filter(email=email).count() == 0 or (User.objects.get(email=email) == request.user):
                form.add_error('email', "Invalid user")
                return redirect('friend_request') 
              user = User.objects.get(email = email)
              new_friend = FriendRequest.objects.create(
                from_user = from_user,
                to_user = user,
                is_active = True)
        new_friend.save()
        return redirect('profile') 
    return render(request, 'friend_request.html', {'form': form})

def accept_request(request, request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id = request_id)
        #add who sent the request to the recipient's friend list
        friend_request.to_user.friends.add(friend_request.from_user)
        #add the recipient to the sender's friend list
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.is_active = False
        friend_request.delete()

def decline_request(request, request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id = request_id)
        friend_request.is_active = False
        friend_request.delete()


            
                

    