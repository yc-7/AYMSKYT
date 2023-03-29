from django.shortcuts import redirect
from minted.forms import NotificationSubscriptionForm
from minted.mixins import AdminProhibitedMixin
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from minted.notifications import unsubscribe_user_from_push, delete_user_subscriptions

class NotificationSubscriptionCreateView(AdminProhibitedMixin, CreateView):
    """View to create a new notification subscription"""

    template_name = 'notification_subscriptions/create_notification_subscription.html'
    form_class = NotificationSubscriptionForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = self.request.user
        notification_subscription = form.save()
        user.notification_subscription = notification_subscription
        user.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.notification_subscription != None:
            return redirect('edit_notification_subscription')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.user.notification_subscription != None:
            return redirect('edit_notification_subscription')
        return super().post(request, *args, **kwargs)
    
class NotificationSubscriptionUpdateView(AdminProhibitedMixin, UpdateView):
    """View to update an existing notification subscription"""

    form_class = NotificationSubscriptionForm
    template_name = 'notification_subscriptions/edit_notification_subscription.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Return the NotificationSubscription to be updated"""
        user = self.request.user
        return user.notification_subscription

    def form_valid(self, form):
        if not self.object:
            return redirect('create_notification_subscription')
        response = super().form_valid(form)
        messages.success(self.request, "Notification subscription updated successfully.")
        return response
    
class PushSubscriptionDeleteView(AdminProhibitedMixin, View):
    """View to delete push subscription"""

    http_method_name = ['post']

    def post(self, request):
        user = self.request.user
        delete_user_subscriptions(user)
        unsubscribe_user_from_push(request.user.id)
        
        return redirect('profile')
