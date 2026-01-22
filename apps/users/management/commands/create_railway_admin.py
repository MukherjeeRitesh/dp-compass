"""
Management command to create a superuser for Railway deployment if none exists.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser for Railway deployment if one does not exist'

    def handle(self, *args, **options):
        # Check if any admin user exists
        if User.objects.filter(role='admin').exists():
            self.stdout.write(self.style.SUCCESS('Admin user already exists, skipping creation.'))
            return
        
        # Get credentials from environment variables
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
        email = config('DJANGO_SUPERUSER_EMAIL', default='admin@dpcompass.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='Admin123!')
        
        # Create the superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
