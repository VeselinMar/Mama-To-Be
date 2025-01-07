from django.db import models


class CategoryChoices(models.TextChoices):
    FOOD = 'Food', 'Food'
    PREGNANCY = 'Pregnancy', 'Pregnancy'
    SLEEP = 'Sleep', 'Sleep'
    BEHAVIOUR = 'Behaviour', 'Behaviour'
    NONE = 'None', 'None'
    HEALTH = 'Health', 'Health'
    DIET_NUTRITION = 'Diet & Nutrition', 'Diet & Nutrition'
    FITNESS = 'Fitness', 'Fitness'
    WORK_LIFE_BALANCE = 'Work-Life Balance', 'Work-Life Balance'
    TOYS_PLAY = 'Toys & Play', 'Toys & Play'
    SAFETY = 'Safety', 'Safety'
    FAMILY_TRAVEL = 'Family Travel', 'Family Travel'
    CLOTHING = 'Clothing', 'Clothing'
    MENTAL_HEALTH = 'Mental Health', 'Mental Health'
    BABY_GEAR = 'Baby Gear', 'Baby Gear'
    EDUCATION = 'Education', 'Education'
    RELATIONSHIP_ADVICE = 'Relationship Advice', 'Relationship Advice'
