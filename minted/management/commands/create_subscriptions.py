from django.core.management.base import BaseCommand
from minted.models import Subscription

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Subscription.objects.create(
            name = 'Budgets',
            description = "Alerts for staying on and going over budgets"
        )

        Subscription.objects.create(
            name = 'Friend Requests'
        )
        print("Created subscriptions")



