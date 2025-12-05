from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryChoices(models.TextChoices):
    FOOD = 'Food', _('Food')
    PREGNANCY = 'Pregnancy', _('Pregnancy')
    SLEEP = 'Sleep', _('Sleep')
    BEHAVIOUR = 'Behaviour', _('Behaviour')
    NONE = 'None', _('None')
    HEALTH = 'Health', _('Health')
    DIET_NUTRITION = 'Diet & Nutrition', _('Diet & Nutrition')
    FITNESS = 'Fitness', _('Fitness')
    TOYS_PLAY = 'Toys & Play', _('Toys & Play')
    SAFETY = 'Safety', _('Safety')
    FAMILY_TRAVEL = 'Family Travel', _('Family Travel')
    CLOTHING = 'Clothing', _('Clothing')
    MENTAL_HEALTH = 'Mental Health', _('Mental Health')
    BABY_GEAR = 'Baby Gear', _('Baby Gear')
    EDUCATION = 'Education', _('Education')
    RELATIONSHIP = 'Relationship', _('Relationship')