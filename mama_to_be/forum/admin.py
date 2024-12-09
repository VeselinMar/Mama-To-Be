from django.contrib import admin

from mama_to_be.forum.models import Category, Topic, Discussion, Comment, Like


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_by', 'created_at')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_by',)
    search_fields = ('title', 'category__name', 'created_by__username')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_by', 'created_at')
    search_fields = ('content', 'created_by__username')
    readonly_fields = ('created_by',)
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'discussion', 'created_by', 'parent', 'created_at', 'likes')
    search_fields = ('content', 'created_by__username')
    list_filter = ('created_at', 'likes')
    raw_id_fields = ('parent',)  # Makes it easier to select parent comments


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('comment__content', 'user')
    search_fields = ('comment__content', 'user__username')

