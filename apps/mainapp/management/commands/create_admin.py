from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mainapp.models import UserProfile


class Command(BaseCommand):
    help = 'Create an admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--email', type=str, default='admin@example.com', help='Admin email')
        parser.add_argument('--password', type=str, default='admin123', help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            # Update existing user's password and profile to be admin
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            # Update or create user profile with admin role
            UserProfile.objects.update_or_create(user=user, defaults={'role': 'admin'})
            self.stdout.write(self.style.SUCCESS(f'Updated {username} to admin with new password!'))
            return

        # Create new admin user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create user profile with admin role
        UserProfile.objects.create(user=user, role='admin')
        
        self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created successfully!'))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write('Login at: /login/')
