from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mainapp.models import UserProfile


class Command(BaseCommand):
    help = 'Fix admin profiles - ensures all superusers have admin role in their UserProfile'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        # Get all superusers
        superusers = User.objects.filter(is_superuser=True)
        
        if not superusers.exists():
            self.stdout.write(self.style.WARNING('No superusers found in the database.'))
            return
        
        self.stdout.write(f'Found {superusers.count()} superuser(s)')
        
        updated_count = 0
        for user in superusers:
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            if profile.role != 'admin':
                if dry_run:
                    self.stdout.write(
                        f'[DRY RUN] Would update {user.username}: role "{profile.role}" -> "admin"'
                    )
                else:
                    profile.role = 'admin'
                    profile.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated {user.username}: role "{profile.role}" -> "admin"')
                    )
                updated_count += 1
            else:
                self.stdout.write(
                    f'{user.username}: role is already "admin" (no change needed)'
                )
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'[DRY RUN] Would have updated {updated_count} profile(s)'))
        else:
            if updated_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated {updated_count} profile(s) to admin role!')
                )
            else:
                self.stdout.write('All superusers already have admin role.')
