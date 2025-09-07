from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from mama_to_be.common.signals import dump_seed
from mama_to_be.common.github import commit_seed_to_github

from mama_to_be.profiles.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if DISABLE_SEED_SIGNALS:
        return
    if created:
        Profile.objects.update_or_create(user=instance)

@receiver([post_save], sender=UserModel)
def user_changed(sender, **kwargs):
    if DISABLE_SEED_SIGNALS:
        return
    dump_seed()
    commit_seed_to_github()