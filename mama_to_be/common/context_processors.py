from django.core.cache import cache

from mama_to_be.articles.choices import CategoryChoices
from mama_to_be.articles.models import Article


def navbar_data(request):
    # Check if navbar data is cached
    navbar = cache.get('navbar_data')

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

    return {
        'navbar_categories': navbar,
    }
