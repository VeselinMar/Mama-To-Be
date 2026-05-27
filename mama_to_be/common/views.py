from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.views import View
from django.http import Http404, JsonResponse
from django.core.files.storage import default_storage
from .utility import process_image_to_webp
from ..articles.models import Article
from ..food.models import Recipe
from django.utils.translation import get_language
from concurrent.futures import ThreadPoolExecutor

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector
)
from django.shortcuts import render

import traceback


# Create your views here.

class HomeView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        language = get_language()

        context["latest_article"] = (
            Article.objects.translated(language_code=language)
            .select_related("author")
            .order_by("-created_at")
            .first()
        )

        context["latest_recipe"] = (
            Recipe.objects.translated(language_code=language)
            .select_related("author")
            .prefetch_related(
                "tags",
                "ingredients",
            )            
            .order_by("-created_at")
            .first()
        )

        return context

class PrivacyView(TemplateView):
    template_name = 'common/footer_related/privacy.html'

class ImpressumView(TemplateView):
    template_name = 'common/footer_related/impressum.html'

class ContactView(TemplateView):
    template_name = 'common/footer_related/contact.html'

class AboutView(TemplateView):
    template_name = 'common/footer_related/about.html'

@require_POST
def upload_image(request):
    print("METHOD:", request.method)

    uploaded_file = request.FILES.get("file")
    print("FILES:", request.FILES)
    print("POST:", request.POST)
    print("CONTENT TYPE:", request.content_type)
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        content_file = process_image_to_webp(uploaded_file)
        path = default_storage.save(content_file.name, content_file)
        url = default_storage.url(path)

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"location": url})

def lang_to_pg_config(lang_code):
    mapping = {
        'en': 'english', 'de': 'german',
    }
    base = lang_code.split('-')[0].lower()
    return mapping.get(base, 'simple')

def search_view(request):
    q = request.GET.get('q', '').strip()
    lang = request.LANGUAGE_CODE
    config = lang_to_pg_config(lang)

    results = []

    if q:
        query = SearchQuery(q, config=config, search_type='websearch')

        vector_article = (
            SearchVector('translations__title', weight='A', config=config) +
            SearchVector('translations__content', weight='B', config=config)
        )
        vector_recipe = (
            SearchVector('translations__name', weight='A', config=config) +
            SearchVector('translations__text', weight='B', config=config)
        )

        article_qs = (
            Article.objects.language(lang)
            .filter(is_published=True)
            .annotate(rank=SearchRank(vector_article, query))
            .filter(rank__gt=0)
            .order_by('-rank')[:10]
        )

        recipe_qs = (
            Recipe.objects.language(lang)
            .annotate(rank=SearchRank(vector_recipe, query))
            .filter(rank__gt=0)
            .order_by('-rank')[:10]
        )

        with ThreadPoolExecutor(max_workers=2) as executor:
            future_articles = executor.submit(list, article_qs)
            future_recipes = executor.submit(list, recipe_qs)
            articles = future_articles.result()
            recipes = future_recipes.result()

        results = (
            [{'type': 'article', 'obj': a, 'rank': a.rank} for a in articles] +
            [{'type': 'recipe',  'obj': r, 'rank': r.rank} for r in recipes]
        )
        results.sort(key=lambda x: x['rank'], reverse=True)

    return render(request, 'common/search_results.html', {'results': results, 'query': q})