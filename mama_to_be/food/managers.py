from django.db import models
from django.db.models import Count, Q


class RecipeQuerySet(models.QuerySet):
    def with_ingredients(self, ingredients):
        """
        Filter recipes that use at least one of the given ingredients.
        `ingredients` can be a list/queryset of Ingredient objects or IDs.
        """
        ingredient_ids = [i.id if hasattr(i, 'id') else i for i in ingredients]
        return self.filter(ingredients__id__in=ingredient_ids)

    def similar_to(self, recipe):
        """
        Returns recipes sharing at least one ingredient with `recipe`,
        excluding the recipe itself, ordered by number of shared ingredients.
        """
        ingredient_ids = recipe.ingredients.values_list('id', flat=True)
        return (
            self.with_ingredients(ingredient_ids)
            .exclude(id=recipe.id)
            .annotate(shared_count=Count('ingredients', filter=Q(ingredients__in=recipe.ingredients.all()), distinct=True))
            .order_by('-shared_count', '-created_at')
        )

class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def similar_to(self, recipe):
        return self.get_queryset().similar_to(recipe)
