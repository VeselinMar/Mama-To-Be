import uuid

from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

from mama_to_be import settings
from mama_to_be.articles.choices import CategoryChoices
from mama_to_be.articles.managers import ArticleQuerySet


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = HTMLField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    media_urls = models.TextField(blank=True, null=True)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(
        max_length=25,
        choices=CategoryChoices.choices,
        default=CategoryChoices.NONE,
    )
    is_published = models.BooleanField(default=False)

    # Attach the custom queryset
    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return self.title

    def generate_unique_slug(self):
        """Generates a unique slug for the article."""
        if not self.slug:
            self.slug = slugify(self.title)

        original_slug = self.slug
        queryset = Article.objects.filter(slug=self.slug)
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        while queryset.exists():
            self.slug = f"{original_slug}-{uuid.uuid4().hex[:8]}"
            queryset = Article.objects.filter(slug=self.slug)

    def save(self, *args, **kwargs):
        """Overrides the default save method to ensure unique slugs."""
        self.generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']
