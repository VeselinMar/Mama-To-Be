from django.shortcuts import render

from mama_to_be.articles.models import Article


# Create your views here.


def home(request):
    recent_articles = (
        Article.objects.filter(is_published=True)
        .distinct('category')
        .order_by('category', '-published_at')[:12]
    )

    articles_by_category = {}
    for article in recent_articles:
        if article.category not in articles_by_category:
            articles_by_category[article.category] = []
        articles_by_category[article.category].append(article)

    context = {
        'articles_by_category': articles_by_category,
    }
    return render(request, 'common/home.html', context)
