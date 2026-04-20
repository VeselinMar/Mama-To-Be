from django.db import models
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
    # Mass
    GRAM = "g", "Gram (g)"
    KILOGRAM = "kg", "Kilogram (kg)"

    # Volume
    MILLILITER = "ml", "Milliliter (ml)"
    LITER = "l", "Liter (l)"
    CUP = "cup", "Cup"
    TABLESPOON = "tbsp", "Tablespoon"
    TEASPOON = "tsp", "Teaspoon"

    # Count / informal
    PIECE = "pc", "Piece"
    PINCH = "pinch", "Pinch"
    DASH = "dash", "Dash"
    CLOVE = "clove", "Clove"
    SLICE = "slice", "Slice"