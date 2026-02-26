from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from django import forms
from .models import Article
from parler.forms import TranslatableModelForm



class ArticleForm(TranslatableModelForm):
    MAX_URLS = 10
    MAX_URL_LENGTH = 500  # Limit URL length

    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'is_published', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
