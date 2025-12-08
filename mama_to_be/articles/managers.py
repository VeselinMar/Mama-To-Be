from parler.managers import TranslatableManager, TranslatableQuerySet

class ArticleQuerySet(TranslatableQuerySet):
    def published(self):
        return self.filter(is_published=True)

    def in_category(self, category):
        return self.published().filter(category=category)