from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from mama_to_be.food.models import Recipe, Food

# Create your views here.

class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new Recipe. Only accessible to logged-in users.
    """
    model = Recipe