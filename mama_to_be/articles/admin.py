from django.contrib import admin

from mama_to_be.articles.models import Article


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'published_at', 'created_at')
    list_filter = ('is_published', 'category', 'created_at', 'published_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_at',)
    readonly_fields = ('created_at', 'updated_at', 'author')

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'category', 'thumbnail_url', 'media_urls')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
