from django.db import models
from django.utils.text import slugify

from mama_to_be.settings import AUTH_USER_MODEL


# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'  # Correct pluralization


class Topic(models.Model):
    title = models.CharField(
        max_length=130,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='topics')
    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='topics')
    created_at = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Discussion(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="discussions"
    )
    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Discussion on {self.topic.title}"


class Comment(models.Model):

    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    content = models.TextField(
        max_length=800,
    )

    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.created_by} on {self.topic.title}"


class Like(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_likes')
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='liked_by'
    )

    class Meta:
        unique_together = ('comment', 'user')
