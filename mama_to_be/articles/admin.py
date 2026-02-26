from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Article

@admin.register(Article)
class ArticleAdmin(TranslatableAdmin):
    list_display = ('title', 'author', 'published_at', 'category', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('translations__title', 'translations__content')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'author', 'category', 'is_published', 'thumbnail_url', 'thumbnail')
        }),
    )