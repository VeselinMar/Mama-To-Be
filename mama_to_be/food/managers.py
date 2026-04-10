from django.db import models
from django.db.models import Count, Q

from parler.managers import TranslatableQuerySet, TranslatableManager

class RecipeQuerySet(TranslatableQuerySet):
    def with_ingredients(self, ingredients):
        ingredient_ids = [i.id if hasattr(i, 'id') else i for i in ingredients]
        return self.filter(ingredients__id__in=ingredient_ids)

    def similar_to(self, recipe):
        ingredient_ids = recipe.ingredients.values_list('id', flat=True)
        return (
            self.with_ingredients(ingredient_ids)
            .exclude(id=recipe.id)
            .annotate(
                shared_count=Count(
                    'ingredients',
                    filter=Q(ingredients__in=recipe.ingredients.all()),
                    distinct=True
                )
            )
            .order_by('-shared_count', '-created_at')
        )

    def search(self, query):
        return self.filter(
            Q(translations__name__icontains=query) |
            Q(translations__text__icontains=query)
        )