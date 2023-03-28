from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings

class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        self.create_sites()
        google = SocialApp.objects.create(
            provider='google',
            name='google',
            client_id=f'{settings.CLIENT_ID}',
            secret=f'{settings.SECRET}',
            key='',
        )
        sites = Site.objects.all()
        google.sites.set(sites)
        google.save()
        print("Social App 'google' added")
    
    def create_sites(self):
        example = Site.objects.get(domain='example.com')
        example.domain = 'http://localhost:8000'
        example.name = 'http://localhost:8000'
        example.save()
        Site.objects.create(
            domain='http://127.0.0.1:8000',
            name='http://127.0.0.1:8000'
        )
        site = settings.CSRF_TRUSTED_ORIGINS[0]
        Site.objects.create(
            domain=f'{site}',
            name=f'{site}'
        )
