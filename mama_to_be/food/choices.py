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