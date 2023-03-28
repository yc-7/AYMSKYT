from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.create_sites()
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
    
    def create_sites(self):
        example = Site.objects.filter(domain_name='example.com')
        if example.exists():
            example.first().delete()
        for site in settings.CSRF_TRUSTED_ORIGINS:
            Site.objects.create(
                domain_name=f'{site}',
                display_name=f'{site}'
            )
        Site.objects.create(
            domain_name='http://localhost:8000'
            display_name='http://localhost:8000'
        )
        Site.objects.create(
            domain_name='http://127.0.0.1:8000'
            display_name='http://127.0.0.1:8000'
        )
