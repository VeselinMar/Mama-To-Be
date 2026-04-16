import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from tinymce.models import HTMLField
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from parler.utils.context import switch_language
from slugify import slugify

from .choices import AllergenChoices, RecipeType, DifficultyChoices
from .managers import RecipeQuerySet  # Assuming you have a custom queryset
from ..common.models import Tag
from mama_to_be.common.utility import process_image_to_webp


LANGUAGES = [lang[0] for lang in settings.LANGUAGES]


# -------------------
# INGREDIENT
# -------------------
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # macros per 100g
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)

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
class Recipe(TranslatableModel):

    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        slug=models.SlugField(unique=False, blank=True, null=True),  # Added unique=False
        text=HTMLField(blank=True),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        blank=True,
        null=True,
        help_text="Upload a thumbnail image for this recipe"
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipe_type = models.CharField(
        max_length=15,
        choices=RecipeType.choices,
        blank=True,
        null=True
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.EASY
    )

    # Time
    prep_time = models.PositiveIntegerField(null=True, blank=True)
    cook_time = models.PositiveIntegerField(null=True, blank=True)

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )

    # Tags (common.models.tags)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes'
    )

    servings = models.PositiveIntegerField(default=4)

    # Ratings
    avg_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    # Use TranslatableManager with custom queryset (if you have one)
    # If you don't have RecipeQuerySet, use: objects = TranslatableManager()
    objects = TranslatableManager.from_queryset(RecipeQuerySet)()

    class Meta:
        ordering = ['-created_at']

    def _convert_to_grams(self, quantity, unit):
        if not quantity:
            return 0

        if not unit:
            return quantity

        unit = unit.lower()

        conversions = {
            "g": 1,
            "gram": 1,
            "grams": 1,

            "kg": 1000,

            "ml": 1,
            "l": 1000,

            "cup": 240,
            "tbsp": 15,
            "tsp": 5,
        }

        return quantity * conversions.get(unit, 0)  # unknown unit → 0

    
    @property
    def total_macros(self):
        protein = 0
        carbs = 0
        fat = 0

        for ri in self.recipeingredient_set.all():
            grams = self._convert_to_grams(ri.quantity, ri.unit)

            if grams == 0:
                continue

            factor = grams / 100

            protein += ri.ingredient.protein * factor
            carbs += ri.ingredient.carbs * factor
            fat += ri.ingredient.fat * factor

        return {
            "protein": round(protein, 2),
            "carbs": round(carbs, 2),
            "fat": round(fat, 2),
        }
    
    @property
    def total_calories(self):
        macros = self.total_macros
        return round(
            macros["protein"] * 4 +
            macros["carbs"] * 4 +
            macros["fat"] * 9,
            2
        )

    @property
    def calories_per_serving(self):
        return round(self.total_calories / self.servings, 2)
    
    @property
    def total_time(self):
        return (self.prep_time or 0) + (self.cook_time or 0)


    def __str__(self):
        return self.safe_translation_getter('name', default="(no name)")

    def generate_unique_slug(self):
        name = self.safe_translation_getter("name", any_language=True)
        if not name:
            return

        base_slug = slugify(name)[:50]
        if not base_slug:
            base_slug = uuid.uuid4().hex[:8]

        lang = self.get_current_language()

        queryset = Recipe.objects.translated(lang, slug=base_slug)
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        final_slug = base_slug

        while queryset.exists():
            suffix = uuid.uuid4().hex[:6]
            base = base_slug[:50 - len(suffix) - 1]
            final_slug = f"{base}-{suffix}"
            queryset = Recipe.objects.translated(lang, slug=final_slug)

        self.set_current_language(lang)
        self.slug = final_slug

    def save(self, *args, **kwargs):
        current_lang = self.get_current_language()

        # Generate slug for current language
        if not self.safe_translation_getter("slug"):
            self.generate_unique_slug()

        # Ensure slug for all languages
        for lang in LANGUAGES:  # Fixed: use LANGUAGES list
            with switch_language(self, lang):
                if not self.safe_translation_getter("name"):
                    continue
                if not self.safe_translation_getter("slug"):
                    self.generate_unique_slug()

        self.set_current_language(current_lang)

        if self.thumbnail and not self.thumbnail.name.lower().endswith(".webp"):
            self.thumbnail = process_image_to_webp(self.thumbnail)

        super().save(*args, **kwargs)
    
# -------------------
# RECIPE INGREDIENT
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
        recipe_name = self.recipe.safe_translation_getter('name', default='Unknown Recipe')
        return f"{self.quantity}{self.unit} {self.ingredient.name} in {recipe_name}"


# -------------------
# USER INTERACTION
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
        recipe_name = self.recipe.safe_translation_getter('name', default='Unknown Recipe')
        return f"{recipe_name} on day {self.day} ({self.meal_type})"