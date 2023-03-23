from django.core.management.base import BaseCommand
from django.apps import apps
from webpush.models import PushInformation, SubscriptionInfo
from minted.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Unseeding data...")
        web_push_models = [PushInformation, SubscriptionInfo]
        models = apps.get_app_config('minted').get_models()
        
        for model in models:
            if model == User:
                continue
            model.objects.all().delete()
        for model in web_push_models:
            model.objects.all().delete()
        
        # Delete all non superuser users
        User.objects.all().filter(is_superuser = False).delete()
        print("Done")