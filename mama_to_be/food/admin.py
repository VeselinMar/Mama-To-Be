from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeInteraction,
    MealPlan,
    MealPlanItem,
)
from ..common.models import Tag


# -------------------
# INGREDIENT
# -------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "protein", "carbs", "fat", "calories")
    search_fields = ("name",)
    # Only actual model fields
    list_filter = ("protein", "carbs", "fat")


# -------------------
# TAG
# -------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# -------------------
# RECIPE INGREDIENT INLINE
# -------------------
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ("ingredient",)


# -------------------
# RECIPE INTERACTION INLINE
# -------------------
class RecipeInteractionInline(admin.TabularInline):
    model = RecipeInteraction
    extra = 0
    readonly_fields = (
        "user",
        "rating",
        "is_favorite",
        "cook_count",
        "last_cooked",
    )
    can_delete = False


# -------------------
# RECIPE
# -------------------
@admin.register(Recipe)
class RecipeAdmin(TranslatableAdmin):
    list_display = (
        "get_name",
        "difficulty",
        "total_time_display",
    )

    list_filter = (
        "difficulty",
        "tags",
    )

    search_fields = (
        "translations__name",
        "translations__text",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        RecipeIngredientInline,
        RecipeInteractionInline,
    ]

    fieldsets = (
        ("Title", {"fields": ("name",)}),
        ("Slug", {"fields": ("slug",)}),
        ("Content", {"fields": ("text",)}),
        ("Basic Info", {"fields": ("difficulty",)}),
        ("Time", {"fields": ("prep_time", "cook_time")}),
        ("Tags", {"fields": ("tags",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)
    get_name.short_description = "Name"

    def total_time_display(self, obj):
        return f"{obj.total_time} min"
    total_time_display.short_description = "Total Time"


# -------------------
# RECIPE INGREDIENT
# -------------------
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity", "unit")
    search_fields = (
        "recipe__translations__name",
        "ingredient__name",
    )
    autocomplete_fields = ("recipe", "ingredient")


# -------------------
# RECIPE INTERACTION
# -------------------
@admin.register(RecipeInteraction)
class RecipeInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
        "rating",
        "is_favorite",
        "cook_count",
        "last_cooked",
    )

    list_filter = (
        "rating",
        "is_favorite",
    )

    search_fields = (
        "user__username",
        "recipe__translations__name",
    )

    autocomplete_fields = ("user", "recipe")


# -------------------
# MEAL PLAN ITEM INLINE
# -------------------
class MealPlanItemInline(admin.TabularInline):
    model = MealPlanItem
    extra = 1
    autocomplete_fields = ("recipe",)


# -------------------
# MEAL PLAN
# -------------------
@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ("id",)  # Use id if week_start/created_at don't exist
    search_fields = ("id",)  # Required for autocomplete references
    inlines = [MealPlanItemInline]


# -------------------
# MEAL PLAN ITEM
# -------------------
@admin.register(MealPlanItem)
class MealPlanItemAdmin(admin.ModelAdmin):
    list_display = ("meal_plan", "recipe", "meal_type")
    list_filter = ("meal_type",)
    search_fields = ("meal_plan__id", "recipe__translations__name")
    autocomplete_fields = ("meal_plan", "recipe")