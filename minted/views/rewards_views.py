from django.shortcuts import redirect, render
from minted.decorators import staff_prohibited, staff_required
from minted.forms import *
from minted.models import *
from .general_user_views.login_view_functions import *
from django.contrib import messages
from django.db.models import Q
import datetime


@staff_prohibited
def rewards_homepage(request):
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    rewards = Reward.objects.all().annotate(claimed=Q(reward_id__in=list(user_claims)))
    date = datetime.date.today()
    brands = Reward.objects.all().values_list('brand_name', flat=True).distinct()
    return render(request, 'rewards/rewards_home.html', { 'rewards': rewards, 'date': date, 'brands': brands, 'user': request.user })

@staff_prohibited
def claim_reward(request, brand_name, reward_id):
    if reward_id not in Reward.objects.all().values_list('reward_id', flat=True):
        return redirect('rewards')
    
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    reward = Reward.objects.get(reward_id=reward_id)
    if reward.reward_id in user_claims:
        reward_claim = RewardClaim.objects.get(user=request.user, reward_type__reward_id=reward_id)
        return render(request, 'rewards/rewards_claim.html', { 'reward': reward, 'reward_claim': reward_claim })
    
    user = request.user
    if reward.points_required > user.points:
        return redirect('rewards')
    
    if reward.user_limit == None or reward.user_limit and reward.user_limit > 0:
        reward_claim = RewardClaim.objects.create(reward_type=reward, user=request.user)
        user.points = user.points - reward.points_required
        user.save()
        if reward.user_limit:
            reward.user_limit = reward.user_limit - 1
            reward.save()
        return render(request, 'rewards/rewards_claim.html', { 'reward': reward, 'reward_claim': reward_claim })
    else:
        return redirect('rewards')

@staff_prohibited
def my_rewards(request):
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    claimed_rewards = Reward.objects.filter(Q(reward_id__in=list(user_claims)))
    date = datetime.date.today()
    return render(request, 'rewards/my_rewards.html', { 'claimed_rewards': claimed_rewards, 'date': date })

@staff_prohibited
def filtered_rewards(request, brand_name):
    if Reward.objects.filter(brand_name=brand_name).count() == 0:
        return redirect('rewards')
    user_claims = RewardClaim.objects.filter(user=request.user).values_list('reward_type__reward_id', flat=True)
    rewards = Reward.objects.filter(brand_name=brand_name).annotate(claimed=Q(reward_id__in=list(user_claims)))
    date = datetime.date.today()
    brands = Reward.objects.exclude(brand_name=brand_name).values_list('brand_name', flat=True).distinct()
    return render(request, 'rewards/rewards_home.html', { 'rewards': rewards, 'date': date , 'brands': brands, 'brand_name': brand_name })

@staff_required
def add_rewards(request):
    if request.method == 'POST':
        form = RewardForm(request.POST)
        limit_form = RewardUserLimitForm(request.POST)
        if form.is_valid() and limit_form.is_valid():
            reward = form.save(commit=False)
            reward.user_limit = limit_form.cleaned_data['user_limit']
            reward.save()
            messages.add_message(request, messages.SUCCESS, "Reward successfully created")
            return redirect('rewards_list') 
    else:
        form = RewardForm()
        limit_form = RewardUserLimitForm()
    return render(request, 'rewards/add_rewards.html', {'form': form, 'limit_form': limit_form})

@staff_required
def rewards_list(request):
    if request.method == 'POST':
        if request.POST.get("delete"):
            reward_id = request.POST.get("delete")
            Reward.objects.get(id=reward_id).delete()
            messages.add_message(request, messages.SUCCESS, "Reward deleted successfully")
        return redirect('rewards_list')
    rewards = Reward.objects.all()
    return render(request, 'rewards/rewards_list.html', {'rewards': rewards})

@staff_required
def edit_rewards(request, reward_id):
    if len(Reward.objects.filter(id=reward_id)) == 0:
        return redirect('rewards_list')
    
    reward = Reward.objects.get(id=reward_id)

    if request.method == 'POST':
        form = RewardForm(request.POST, instance = reward)
        limit_form = RewardUserLimitForm(request.POST, instance=reward)
        if form.is_valid() and limit_form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Reward updated!")
            reward = form.save(commit=False)
            reward.user_limit = limit_form.cleaned_data['user_limit']
            reward.save()
            return redirect('rewards_list')
    else:
        form = RewardForm(instance = reward)
        limit_form = RewardUserLimitForm(instance = reward)
    return render(request, 'rewards/edit_rewards.html', {'form': form, 'limit_form': limit_form, 'reward_id': reward.id})

    

