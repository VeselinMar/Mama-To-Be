from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver

from mama_to_be.articles.models import Article


@receiver(post_save, sender=Article)
def update_search_vector_on_save(sender, instance, **kwargs):
    instance.search_vector = (
        SearchVector('title', weight='A') + SearchVector('content', weight='B')
    )
    instance.save()
