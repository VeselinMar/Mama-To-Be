from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
import json

from parler.utils.context import switch_language

from .choices import UnitChoices
from .models import Recipe, Ingredient, RecipeIngredient
from .forms import RecipeForm
from mama_to_be.profiles.models import Profile


import json
from django.db import transaction

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "food/create_recipe_form.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("food:recipe-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unit_choices"] = UnitChoices.choices
        return context

    def form_valid(self, form):
        # Get ingredients from JSON field

        ingredients_json = self.request.POST.get('ingredients_json', '[]')
        print("RAW ingredients_json:")
        print(repr(ingredients_json))
        try:
            ingredients_data = json.loads(ingredients_json)
        except json.JSONDecodeError:
            messages.error(self.request, "Invalid ingredients data")
            return self.form_invalid(form)
        
        # Set author
        form.instance.author = self.request.user
        
        with transaction.atomic():
            self.object = form.save()
            
            for item in ingredients_data:
                ingredient_id = item.get('ingredient_id')
                if not ingredient_id:
                    continue
                
                try:
                    ingredient = Ingredient.objects.get(id=ingredient_id)
                    RecipeIngredient.objects.create(
                        recipe=self.object,
                        ingredient=ingredient,
                        quantity=item.get('quantity') or 0,
                        unit=item.get('unit') or "",
                        note=item.get('note'),
                    )
                except Ingredient.DoesNotExist:
                    continue
        
        messages.success(self.request, "Recipe created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "food/update_recipe_form.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("food:recipe-list")

    def get_object(self):
        lang = self.request.LANGUAGE_CODE
        slug = self.kwargs["slug"]

        return Recipe.objects.language(lang).get(
            translations__slug=slug
        )

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with switch_language(self.object, self.request.LANGUAGE_CODE):
            context["slug"] = self.object.slug

        context["unit_choices"] = UnitChoices.choices

        # preload existing ingredients as JSON
        context["ingredients_json"] = json.dumps([
            {
                "ingredient_id": ri.ingredient.id,
                "name": ri.ingredient.name,
                "quantity": ri.quantity,
                "unit": ri.unit,
                "note": ri.note,
            }
            for ri in self.object.recipeingredient_set.select_related("ingredient")
        ])

        return context

    def form_valid(self, form):
        ingredients_json = self.request.POST.get('ingredients_json', '[]')

        try:
            ingredients_data = json.loads(ingredients_json)
        except json.JSONDecodeError:
            form.add_error(None, "Invalid ingredient data.")
            return self.form_invalid(form)

        with transaction.atomic():
            self.object = form.save()

            # reset old ingredients
            self.object.recipeingredient_set.all().delete()

            for item in ingredients_data:
                ingredient_id = item.get("ingredient_id")

                if not ingredient_id:
                    continue

                ingredient = Ingredient.objects.filter(id=ingredient_id).first()

                if not ingredient:
                    continue

                RecipeIngredient.objects.create(
                    recipe=self.object,
                    ingredient=ingredient,
                    quantity=item.get("quantity") or 0,
                    unit=item.get("unit") or "",
                    note=item.get("note") or "",
                )

        return super().form_valid(form)

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "food/recipe_detail.html"
    context_object_name = "recipe"

    def get_object(self, queryset=None):
        lang = self.request.LANGUAGE_CODE
        slug = self.kwargs["slug"]

        queryset = (
            Recipe.objects
            .active_translations(lang)
            .filter(
                translations__language_code=lang,
                translations__slug=slug
            )
            .select_related("author")
            .prefetch_related(
                "recipeingredient_set__ingredient__translations"
            )
        )

        return get_object_or_404(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object

        author = recipe.author

        if author:
            profile = Profile.objects.filter(user=author).first()
            if profile:
                context["author_name"] = profile.username
                context["author_id"] = profile.user_id

        return context

class RecipeListView(ListView):
    model = Recipe
    template_name = "food/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 9

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE

        return (
            Recipe.objects.active_translations(lang)
            .order_by("-created_at")
        )

def ingredient_autocomplete(request):
    query = request.GET.get("q", "")

    results = []
    if query:
        ingredients = Ingredient.objects.filter(name__icontains=query)[:10]

        results = [
            {"id": ing.id, "text": ing.name}
            for ing in ingredients
        ]

    return JsonResponse({"results": results})

@require_POST
def create_ingredient(request):
    data = json.loads(request.body)

    ingredient, created = Ingredient.objects.get_or_create(
        name=data.get("name"),
        defaults={
            "protein": data.get("protein", 0),
            "carbs": data.get("carbs", 0),
            "fat": data.get("fat", 0),
        }
    )

    return JsonResponse({
        "id": ingredient.id,
        "name": ingredient.name,
        "created": created
    })