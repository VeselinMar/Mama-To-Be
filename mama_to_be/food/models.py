import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from tinymce.models import HTMLField
from .choices import AllergenChoices
from .managers import RecipeManager



# Create your models here.

# Ingredients Model consisting of name / macro and micronutrients / allergens / calories
class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
        )

    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    micros = models.JSONField(
        blank=True,
        null=True,
    )
    
    # SUBSTITUTE 

    allergens = models.JSONField(
        default=list,
        blank=True,
        null=False,
    )
    # allergens = ArrayField(
    #     base_field=models.CharField(
    #         max_length=1,
    #         choices=AllergenChoices.choices,
    #     ),
    #     default=list,
    #     blank=True,
    # )
    
    # calculate calories for 100g when creating a recipe object
    @property
    def calories(self):
        return self.protein * 4 + self.carbs * 4 + self.fat * 9

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        )
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=60
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    text = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )

    objects = RecipeManager()  # <-- use the custom manager

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def generate_unique_slug(self):
        """Generates a unique slug for the recipe."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

        original_slug = self.slug
        queryset = Recipe.objects.filter(slug=self.slug)
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        while queryset.exists():
            suffix = f"-{uuid.uuid4().hex[:8]}"
            max_base_length = 50 - len(suffix)
            base_slug = original_slug[:max_base_length]
            self.slug = f"{base_slug}-{suffix}"
            queryset = Recipe.objects.filter(slug=self.slug)

    def save(self, *args, **kwargs):
        """Overrides the default save method to ensure unique slugs."""
        if not self.slug:
            self.generate_unique_slug()
        super().save(*args, **kwargs)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity or 'Some'} {self.ingredient.name} in {self.recipe.name}"