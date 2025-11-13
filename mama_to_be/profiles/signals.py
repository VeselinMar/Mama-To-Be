from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import mama_to_be.common.utils.signal_control as signal_control
from mama_to_be.profiles.models import Profile, AppUser

UserModel = get_user_model()


@receiver(post_save, sender=AppUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
