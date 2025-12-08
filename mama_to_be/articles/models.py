import uuid

from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import Index

from slugify import slugify
from tinymce.models import HTMLField
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from parler.utils.context import switch_language


from mama_to_be import settings
from mama_to_be.articles.choices import CategoryChoices
from mama_to_be.articles.managers import ArticleQuerySet


# Create your models here.

LANGUAGES = [lang[0] for lang in settings.LANGUAGES]


class Article(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        slug = models.SlugField(unique=False, blank=True, null=True),
        content = HTMLField()
    )
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

    search_vector = SearchVectorField(null=True, blank=True)

    # Attach the custom queryset
    objects = TranslatableManager.from_queryset(ArticleQuerySet)()


    def __str__(self):
        return self.safe_translation_getter('title', default="(no title)")


    def generate_unique_slug(self):
        title = self.safe_translation_getter("title", any_language=True)
        if not title:
            return

        base_slug = slugify(title)[:50]
        if not base_slug:
            base_slug = uuid.uuid4().hex[:8]

        lang = self.get_current_language()

        queryset = Article.objects.translated(lang, slug=base_slug)
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        final_slug = base_slug

        while queryset.exists():
            suffix = uuid.uuid4().hex[:6]
            base = base_slug[:50 - len(suffix) - 1]
            final_slug = f"{base}-{suffix}"
            queryset = Article.objects.translated(lang, slug=final_slug)

        self.set_current_language(lang)
        self.slug = final_slug


    def save(self, *args, **kwargs):
        current_lang = self.get_current_language()

        if not self.safe_translation_getter("slug"):
            self.generate_unique_slug()

        for lang, lang_name in LANGUAGES:
            with switch_language(self, lang):
                    if not self.safe_translation_getter("title"):
                        continue
                    if not self.safe_translation_getter("slug"):
                        self.generate_unique_slug()
        
        self.set_current_language(current_lang)
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']
        indexes = [Index(fields=['search_vector'])]
