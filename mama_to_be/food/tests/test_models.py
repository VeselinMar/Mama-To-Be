import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone

from mama_to_be.food.models import Ingredient, RecipeIngredient, Recipe

class IngredientModelTest(TestCase):
    def setUp(self):
        self.Ingredient = Ingredient.objects.create(
            name="Cheddar",
            protein=18,
            carbs=2,
            fat=40,
            micros={"salt": 6},
            allergens=["MI", "TN"],
        )
    
    def test_ingredient_creation(self):
        self.assertEqual(self.Ingredient.name, "Cheddar")
        self.assertEqual(self.Ingredient.protein, 18)
        self.assertEqual(self.Ingredient.carbs, 2)
        self.assertEqual(self.Ingredient.fat, 40)
        # adjust when migrating to postgresql
        self.assertEqual(self.Ingredient.micros, {"salt": 6})

    def test_calories_property(self):
        expected = 18 * 4 + 2 * 4 + 40 * 9
        self.assertEqual(self.Ingredient.calories, expected)
    # adjust when migrating to postgresql
    def test_allergens_jsonfield(self):
        self.assertListEqual(self.Ingredient.allergens, ["MI", "TN"])

    def test_empty_allergen_default(self):
        """Default allergens should be an empty list, not None."""
        ing = Ingredient.objects.create(
            name="Plain Rice",
            protein=2.5,
            carbs=28,
            fat=0.3,
        )
        self.assertEqual(ing.allergens, [])

    def test_str_representation(self):
        self.assertEqual(str(self.Ingredient), "Cheddar")
