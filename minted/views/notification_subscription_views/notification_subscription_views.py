from django.shortcuts import redirect, render
from minted.decorators import staff_prohibited, login_required
from minted.forms import NotificationSubscriptionForm

@staff_prohibited
def create_notification_subscription(request):
    if request.user.notification_subscription != None:
        return redirect('edit_notification_subscription')

    notification_subscription_form = NotificationSubscriptionForm()
    if request.method == 'POST':
        notification_subscription_form = NotificationSubscriptionForm(request.POST)
        if notification_subscription_form.is_valid():
            notification_subscription = notification_subscription_form.save()

            user = request.user
            user.notification_subscription = notification_subscription
            user.save()

            return redirect('profile')      
    return render(request, 'notification_subscriptions/create_notification_subscription.html', {'form': notification_subscription_form})


@staff_prohibited
def edit_notification_subscription(request):
    user = request.user
    notification_subscription_exists = user.notification_subscription != None
    if not notification_subscription_exists:
        return redirect('create_notification_subscription')
    
    notification_subscription = user.notification_subscription

    form = NotificationSubscriptionForm(instance=notification_subscription)
    if request.method == 'POST':
        form = NotificationSubscriptionForm(request.POST, instance=notification_subscription)
        if form.is_valid():
            notification_subscription = form.save()
            return redirect('profile')
        
    return render(request, 'notification_subscriptions/edit_notification_subscription.html', {'form': form})