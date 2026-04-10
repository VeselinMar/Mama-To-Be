from django.urls import path
from .views import RecipeCreateView, RecipeUpdateView, RecipeListView, RecipeDetailView, ingredient_autocomplete, create_ingredient
from mama_to_be.common.views import upload_image

app_name = "food"

urlpatterns = [
    # recipe admin
    path("recipes/create/", RecipeCreateView.as_view(), name="recipe-create"),
    path("recipes/<slug:slug>/update/", RecipeUpdateView.as_view(), name="recipe-update"),
    # recipe repr
    path("recipes/", RecipeListView.as_view(), name="recipe-list"),
    path("recipes/<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path('upload-image/', upload_image, name='upload-image'),
    # ingredients
    path("ingredients/autocomplete/", ingredient_autocomplete, name="ingredient-autocomplete"),
    path("ingredients/create/", create_ingredient, name="ingredient-create"),
]