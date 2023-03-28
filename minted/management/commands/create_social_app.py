from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        google = SocialApp.objects.create(
            provider='google',
            name='google',
            client_id='390199461456-eaai5hrm5da5q4j61c9l88s8sdqbhnkh.apps.googleusercontent.com',
            secret='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',
            key='',
        )
        sites = Site.objects.all()
        google.sites.set(sites)
        google.save()
        print("Social App 'google' added")