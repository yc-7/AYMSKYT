from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages
from django.db.models import Q
import datetime


@login_required
def rewards_homepage(request):
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    rewards = Reward.objects.all().annotate(claimed=Q(reward_id__in=list(user_claims)))
    date = datetime.date.today()
    brands = Reward.objects.all().values_list('brand_name', flat=True).distinct()
    return render(request, 'rewards/rewards_home.html', { 'rewards': rewards, 'date': date, 'brands': brands })

@login_required
def claim_reward(request, brand_name, reward_id):
    if reward_id not in Reward.objects.all().values_list('reward_id', flat=True):
        return redirect('rewards')
    
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    reward = Reward.objects.get(reward_id=reward_id)
    if reward.reward_id in user_claims:
        reward_claim = RewardClaim.objects.get(user=request.user, reward_type__reward_id=reward_id)
        return render(request, 'rewards/rewards_claim.html', { 'reward': reward, 'reward_claim': reward_claim })
    
    reward_claim = RewardClaim.objects.create(reward_type=reward, user=request.user)
    return render(request, 'rewards/rewards_claim.html', { 'reward': reward, 'reward_claim': reward_claim })

@login_required
def my_rewards(request):
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    claimed_rewards = Reward.objects.filter(Q(reward_id__in=list(user_claims)))
    date = datetime.date.today()
    return render(request, 'rewards/my_rewards.html', { 'claimed_rewards': claimed_rewards, 'date': date })

@login_required
def filtered_rewards(request, brand_name):
    if Reward.objects.filter(brand_name=brand_name).count() == 0:
        return redirect('rewards')
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    rewards = Reward.objects.filter(brand_name=brand_name).annotate(claimed=Q(reward_id__in=list(user_claims)))
    date = datetime.date.today()
    brands = Reward.objects.exclude(brand_name=brand_name).values_list('brand_name', flat=True).distinct()
    return render(request, 'rewards/rewards_home.html', { 'rewards': rewards, 'date': date , 'brands': brands, 'brand_name': brand_name })


    

