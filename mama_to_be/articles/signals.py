from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mama_to_be.common.signals import dump_seed
from mama_to_be.common.github import commit_seed_to_github

from mama_to_be.articles.models import Article


@receiver(post_save, sender=Article)
def update_search_vector_on_save(sender, instance, **kwargs):
    if 'postgres' in settings.DATABASES['default']['ENGINE']:
        instance.search_vector = (
            SearchVector('title', weight='A') + SearchVector('content', weight='B')
        )
        instance.save()

@receiver([post_save, post_delete], sender=Article)
def article_changed(sender, **kwargs):
    dump_seed()
    commit_seed_to_github()