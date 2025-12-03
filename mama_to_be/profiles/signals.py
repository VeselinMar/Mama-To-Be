from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from mama_to_be.profiles.models import Profile, AppUser


@receiver(post_save, sender=AppUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
