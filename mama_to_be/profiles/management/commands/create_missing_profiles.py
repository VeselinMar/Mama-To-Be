from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mama_to_be.profiles.models import Profile

class Command(BaseCommand):
    help = "Create missing profiles for existing users"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        created_count = 0
        for user in User.objects.all():
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created_count} missing profiles."))