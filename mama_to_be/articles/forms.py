from django import forms
from tinymce.widgets import TinyMCE

from mama_to_be.articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
        model = Article
        fields = ['title', 'content', 'category', 'is_published', 'thumbnail_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter thumbnail URL'}),

        }

    def clean_media_urls(self):
        media_urls = self.cleaned_data.get('media_urls', '')
        if media_urls:
            trusted_domains = ['youtube.com', 'vimeo.com', 'unsplash.com', 'imgur.com', 'shopify.com', 'dupe.com']
            urls = [url.strip() for url in media_urls.split(',')]
            for url in urls:
                if not any(domain in url for domain in trusted_domains):
                    raise forms.ValidationError(f"URL {url} is not from a trusted source.")
        return media_urls
