import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from tinymce.models import HTMLField

from .choices import AllergenChoices, RecipeType
from .managers import RecipeManager


# -------------------
# INGREDIENT
# -------------------
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # macros per 100g
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    micros = models.JSONField(blank=True, null=True)

    allergens = ArrayField(
        base_field=models.CharField(
            max_length=1,
            choices=AllergenChoices.choices,
        ),
        default=list,
        blank=True,
    )

    @property
    def calories(self):
        return self.protein * 4 + self.carbs * 4 + self.fat * 9

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# -------------------
# RECIPE
# -------------------
class Recipe(models.Model):
    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True, blank=True, max_length=60)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    text = HTMLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipe_type = models.CharField(
        max_length=15,
        choices=RecipeType.choices,
        blank=True,
        null=True
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )

    # ⭐ Aggregated stats for fast queries
    avg_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    objects = RecipeManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def generate_unique_slug(self):
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
        if not self.slug:
            self.generate_unique_slug()
        super().save(*args, **kwargs)


# -------------------
# RECIPE INGREDIENT (IMPROVED)
# -------------------
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=20, blank=True, null=True)  # e.g. g, ml, cup

    note = models.CharField(max_length=100, blank=True, null=True)  # optional ("chopped")

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity}{self.unit} {self.ingredient.name} in {self.recipe.name}"


# -------------------
# USER INTERACTION ⭐ (CRITICAL)
# -------------------
class RecipeInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    rating = models.IntegerField(null=True, blank=True)  # 1–5
    is_favorite = models.BooleanField(default=False)

    cook_count = models.IntegerField(default=0)
    last_cooked = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user} -> {self.recipe}"


# -------------------
# MEAL PLANNING
# -------------------
class MealPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_start = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - week of {self.week_start}"


class MealPlanItem(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    meal_plan = models.ForeignKey(
        MealPlan,
        on_delete=models.CASCADE,
        related_name='items'
    )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    day = models.IntegerField()  # 0 = Monday, 6 = Sunday
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)

    class Meta:
        unique_together = ('meal_plan', 'day', 'meal_type')

    def __str__(self):
        return f"{self.recipe} on day {self.day} ({self.meal_type})"