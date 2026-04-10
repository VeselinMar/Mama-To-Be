from django import forms
from parler.forms import TranslatableModelForm
from .models import Recipe


class RecipeForm(TranslatableModelForm):
    class Meta:
        model = Recipe
        fields = [
            'name',
            'text',
            'recipe_type',
            'cook_time',
            'prep_time',
            'difficulty',
            'tags',
            'thumbnail',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control tinymce',
                'rows': 6,
            }),
            'recipe_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }