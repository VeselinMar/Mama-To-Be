from django.views.generic import ListView

from mama_to_be.articles.models import Article


# Create your views here.


class HomeView(ListView):
    model = Article
    template_name = 'common/home.html'
    context_object_name = 'articles'  # For referencing in the template

    def get_queryset(self):
        # Fetch all published articles and order by publication date
        return Article.objects.filter(is_published=True).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Categorize articles by category, limiting to the last 3 articles per category
        articles_by_category = {}

        # Get the last 3 articles for each category
        categories = Article.objects.filter(is_published=True).values('category').distinct()

        for category in categories:
            articles = (
                Article.objects.filter(category=category['category'], is_published=True)
                .order_by('-published_at')[:3]  # Limit to 3 articles per category
            )
            articles_by_category[category['category']] = articles

        context['articles_by_category'] = articles_by_category

        return context
