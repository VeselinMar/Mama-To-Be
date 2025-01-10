from django.core.cache import cache

from mama_to_be.articles.choices import CategoryChoices
from mama_to_be.articles.models import Article


def navbar_data(request):
    # Check if navbar data is cached
    navbar = cache.get('navbar_data')
    helpful_articles = cache.get('helpful_articles')

    if not navbar:
        # Build the navbar data by checking which categories have articles
        navbar = []
        for category in CategoryChoices:
            # Ensure category has 'value' and 'label'
            category_value = getattr(category, 'value', None)
            category_label = getattr(category, 'label', None)

            # Check if articles exist for the category
            if category_value and Article.objects.filter(category=category_value, is_published=True).exists():
                navbar.append({'value': category_value, 'name': category_label})

        # Cache the navbar data
        cache.set('navbar_data', navbar, timeout=3600)  # Cache for 1 hour

    if not helpful_articles:
        # Fetch articles for the "helpful" category
        helpful_articles = Article.objects.filter(
            category=CategoryChoices.HELPFUL, is_published=True
        ).order_by('-published_at')

        # Cache the helpful articles
        cache.set('helpful_articles', helpful_articles, timeout=3600)

    return {
        'navbar_categories': navbar,
        'helpful_articles': helpful_articles,
    }
