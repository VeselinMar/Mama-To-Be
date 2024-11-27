from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

from mama_to_be import settings
from mama_to_be.articles.choices import CategoryChoices


# Create your models here.

class Article(models.Model):
    title = models.CharField(
        max_length=200
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )
    content = HTMLField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    media_urls = models.TextField(
        blank=True,
        null=True,
    )
    thumbnail_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True
    )
    category = models.CharField(
        max_length=25,
        choices=CategoryChoices.choices,
        default=CategoryChoices.NONE
    )
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']
