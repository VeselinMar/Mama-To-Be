from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import RecipeInteraction, Recipe


@receiver(post_save, sender=RecipeInteraction)
def update_recipe_rating(sender, instance, **kwargs):
    if instance.rating is None:
        return 

    recipe = instance.recipe

    stats = RecipeInteraction.objects.filter(
        recipe=recipe,
        rating__isnull=False
    ).aggregate(
        avg=Avg('rating'),
        count=Count('rating')
    )

    Recipe.objects.filter(pk=recipe.pk).update(
        avg_rating=stats['avg'] or 0,
        rating_count=stats['count'] or 0
    )