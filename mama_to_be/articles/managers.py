from django.db import models


class ArticleQuerySet(models.QuerySet):
    def published(self):
        """Returns only published articles."""
        return self.filter(is_published=True)

    def in_category(self, category):
        """Returns published articles in a specific category."""
        return self.published().filter(category=category)
