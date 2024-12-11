from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    MAX_URLS = 10
    MAX_URL_LENGTH = 500  # Limit URL length

    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'is_published', 'thumbnail_url', 'media_urls']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter thumbnail URL'}),
            'media_urls': forms.HiddenInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Enter media URLs (comma separated)'}),
        }

    def clean_url_field(self, field_name, trusted_domains):
        """ Helper method to clean and validate URL fields """
        url_field = self.cleaned_data.get(field_name, '')
        if url_field:
            url = urlparse(url_field)
            # Ensure proper scheme and domain
            if url.scheme not in ['http', 'https']:
                raise ValidationError(f"{field_name} must use a valid scheme (http or https).")
            if not any(domain in url.netloc for domain in trusted_domains):
                raise ValidationError(f"{field_name} must be from a trusted source.")
            # Check URL length
            if len(url_field) > self.MAX_URL_LENGTH:
                raise ValidationError(f"{field_name} exceeds the maximum length of {self.MAX_URL_LENGTH} characters.")
        return url_field

    def clean_media_urls(self):
        """ Clean and validate media_urls field, which is comma-separated """
        media_urls = self.cleaned_data.get('media_urls', '')
        if media_urls:
            trusted_domains = ['youtube.com', 'vimeo.com',
                               'unsplash.com', 'imgur.com', 'shopify.com', 'dupe.com',
                               'shutterstock.com', 'timg.com', 'pinimg.com']
            urls = [url.strip() for url in media_urls.split(',')]

            # Check number of URLs
            if len(urls) > self.MAX_URLS:
                raise ValidationError(f"Too many URLs. Maximum allowed is {self.MAX_URLS}.")

            # Validate each URL scheme
            for url in urls:
                parsed_url = urlparse(url)

                # Ensure the URL starts with http:// or https://
                if parsed_url.scheme not in ['http', 'https']:
                    raise ValidationError(f"URL '{url}' must start with 'http://' or 'https://'.")

                # Ensure the domain is trusted
                if not any(domain in parsed_url.netloc for domain in trusted_domains):
                    raise ValidationError(f"URL '{url}' is not from a trusted source.")

                # Ensure the URL length does not exceed the maximum length
                if len(url) > self.MAX_URL_LENGTH:
                    raise ValidationError(f"URL '{url}' is too long. Max length is {self.MAX_URL_LENGTH} characters.")

        return media_urls

    def clean_thumbnail_url(self):
        """ Clean and validate thumbnail_url using the helper function """
        return self.clean_url_field('thumbnail_url', ['youtube.com', 'vimeo.com',
                                                      'unsplash.com', 'imgur.com', 'shopify.com', 'dupe.com',
                                                      'shutterstock.com', 'timg.com', 'pinimg.com'])
