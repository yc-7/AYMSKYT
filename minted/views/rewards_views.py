from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages
from django.db.models import ExpressionWrapper, Q, BooleanField, Exists


@login_required
def rewards_homepage(request):
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    rewards = Reward.objects.all().annotate(claimed=Q(reward_id__in=list(user_claims)))
    return render(request, 'rewards/rewards_home.html', { 'rewards': rewards, 'user': request.user })

@login_required
def claim_reward(request, brand_name, reward_id):
    if reward_id not in Reward.objects.all().values_list('reward_id', flat=True):
        return redirect('rewards')
    
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    reward = Reward.objects.get(reward_id=reward_id)
    if reward.reward_id in user_claims:
        return redirect('rewards')
    
    reward_claim = RewardClaim.objects.create(reward_type=reward, user=request.user)
    return render(request, 'rewards/rewards_claim.html', { 'reward': reward, 'reward_claim': reward_claim })

@login_required
def my_rewards(request):
    pass

