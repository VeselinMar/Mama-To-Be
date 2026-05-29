from django.db import models

from django.utils.translation import gettext_lazy as _

class AllergenChoices(models.TextChoices):
    GLUTEN = "A", "Cereals containing gluten (wheat, rye, barley, oats)"
    CRUSTACEANS = "B", "Crustaceans (crabs, prawns, lobsters)"
    EGGS = "C", "Eggs"
    FISH = "D", "Fish"
    PEANUTS = "E", "Peanuts"
    SOYBEANS = "F", "Soybeans"
    MILK = "G", "Milk"
    NUTS = "H", (
        "Nuts (almonds, hazelnuts, walnuts, cashews, pecan, brazil, pistachio, macadamia)"
    )
    CELERY = "L", "Celery"
    MUSTARD = "M", "Mustard"
    SESAME = "N", "Sesame seeds"
    SULPHITES = "O", "Sulphur dioxide / sulphites >10 mg/kg or >10 mg/L"
    LUPIN = "P", "Lupin"
    MOLLUSCS = "R", "Molluscs (mussels, oysters, squid, snails)"

class RecipeType(models.TextChoices):
    MEAT = "meat", "Meat"
    FISH = "fish", "Fish"
    VEGETARIAN = "vegetarian", "Vegetarian"
    VEGAN = "vegan", "Vegan"

class DifficultyChoices(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD  = "hard", "Hard"

class UnitChoices(models.TextChoices):
    GRAM = "g", _("g")
    KILOGRAM = "kg", _("kg")

    MILLILITER = "ml", _("ml")
    LITER = "l", _("l")

    CUP = "cup", _("cup")
    TABLESPOON = "tbsp", _("tbsp")
    TEASPOON = "tsp", _("tsp")

    PIECE = "pc", _("piece")
    PINCH = "pinch", _("pinch")
    DASH = "dash", _("dash")
    CLOVE = "clove", _("clove")
    SLICE = "slice", _("slice")