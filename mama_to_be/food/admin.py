from django.contrib import admin
from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeInteraction,
    MealPlan,
    MealPlanItem,
)


# -------------------
# INGREDIENT
# -------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "protein", "carbs", "fat", "calories")
    search_fields = ("name",)
    list_filter = ("allergens",)


# -------------------
# RECIPE INGREDIENT INLINE
# -------------------
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ("ingredient",)


# -------------------
# RECIPE INTERACTION INLINE (read-only insight)
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
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "recipe_type",
        "avg_rating",
        "rating_count",
        "created_at",
    )

    list_filter = (
        "recipe_type",
        "created_at",
    )

    search_fields = (
        "name",
        "text",
    )

    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        RecipeIngredientInline,
        RecipeInteractionInline,
    ]

    autocomplete_fields = ("author",)

    readonly_fields = (
        "avg_rating",
        "rating_count",
        "created_at",
        "updated_at",
    )


# -------------------
# RECIPE INGREDIENT (standalone admin)
# -------------------
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity", "unit")
    search_fields = ("recipe__name", "ingredient__name")
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
        "recipe__name",
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
    list_display = ("user", "week_start", "created_at")

    list_filter = ("week_start",)

    search_fields = ("user__username",)

    inlines = [MealPlanItemInline]

    autocomplete_fields = ("user",)


# -------------------
# MEAL PLAN ITEM
# -------------------
@admin.register(MealPlanItem)
class MealPlanItemAdmin(admin.ModelAdmin):
    list_display = ("meal_plan", "recipe", "day", "meal_type")

    list_filter = ("meal_type", "day")

    search_fields = (
        "meal_plan__user__username",
        "recipe__name",
    )

    autocomplete_fields = ("meal_plan", "recipe")