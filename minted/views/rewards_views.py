from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages


@login_required
def rewards_homepage(request):
    rewards = Reward.objects.all()
    return render(request, 'rewards/rewards_home.html', { 'rewards': rewards })

@login_required
def claim_reward(request, brand_name, reward_id):
    reward = Reward.objects.get(reward_id=reward_id)
    reward_claim = RewardClaim.objects.create(reward_type=reward, user=request.user)
    return render(request, 'rewards/rewards_claim.html', { 'reward': reward, 'reward_claim': reward_claim })

