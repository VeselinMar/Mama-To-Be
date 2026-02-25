from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from django.db.models import Q

from parler.utils.context import switch_language

from mama_to_be.articles.choices import CategoryChoices
from mama_to_be.articles.forms import ArticleForm
from mama_to_be.articles.models import Article
from mama_to_be.profiles.models import Profile

# Create your views here.

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new article. Only accessible to logged-in users.
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article_form.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')
    success_message = "Article created successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Set current language
        form.instance.set_current_language(self.request.LANGUAGE_CODE)
        return super().form_valid(form)


class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to edit an existing article. Only accessible to author.
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article_form.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        lang = self.request.LANGUAGE_CODE
        slug = self.kwargs['slug']

        return get_object_or_404(
            Article.objects.active_translations(lang).filter(
                translations__slug=slug
            )
        )

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user

    def get_success_url(self):
        lang = self.request.LANGUAGE_CODE
        with switch_language(self.object, lang):
            slug = self.object.slug
        return reverse_lazy('article-detail', kwargs={'slug': slug})


class ArticleDisplayView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        lang = self.request.LANGUAGE_CODE
        slug = self.kwargs['slug']

        return get_object_or_404(
            Article.objects.active_translations(lang).filter(
                translations__slug=slug
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        author_profile = Profile.objects.get(user=article.author)
        context['author_name'] = author_profile.username
        context['author_id'] = author_profile.user_id
        return context

class CategoryArticlesView(ListView):
    model = Article
    template_name = 'articles/category_articles.html'
    context_object_name = 'object_list'
    paginate_by = 9

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category not in CategoryChoices.values:
            raise Http404("Invalid category")

        lang = self.request.LANGUAGE_CODE
        return (
            Article.objects.active_translations(lang)
            .filter(category=category, is_published=True)
            .order_by("-published_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context

class RecentArticlesView(ListView):
    model = Article
    template_name = 'common/recent-articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        return (
            Article.objects.active_translations(lang)
            .filter(is_published=True)
            .order_by('-published_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.request.LANGUAGE_CODE

        articles_by_category = {}

        categories = (
            Article.objects.active_translations(lang)
            .values_list('category', flat=True)
            .distinct()
        )

        for category in categories:
            articles_by_category[category] = (
                Article.objects.active_translations(lang)
                .filter(category=category, is_published=True)
                .order_by('-published_at')[:3]
            )

        context['articles_by_category'] = articles_by_category
        return context


def search_view(request, lang=None):
    query = request.GET.get("q", "").strip()
    if not query:
        return render(request, "articles/search_results.html", {"articles": [], "query": ""})

    lang = lang or request.LANGUAGE_CODE

    articles = (
        Article.objects.translated(lang)
        .annotate(search=SearchVector('translations__title', weight='A') +
                              SearchVector('translations__content', weight='B'))
        .filter(search__icontains=query, is_published=True)
        .distinct()
        .order_by('-published_at')
    )

    return render(
        request,
        "articles/search_results.html",
        {
            "articles": articles, 
            "query": query
        }
    )