from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from mama_to_be.articles.choices import CategoryChoices
from mama_to_be.articles.forms import ArticleForm
from mama_to_be.articles.models import Article
from mama_to_be.profiles.models import Profile


# Create your views here.

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article_form.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class ArticleEditView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article_form.html'
    context_object_name = 'article'

    def get_success_url(self):
        # Redirect to the article detail page after successful editing
        return reverse_lazy('article-detail', kwargs={'slug': self.object.slug})

    def dispatch(self, request, *args, **kwargs):
        # Restrict access to the article author only
        article = self.get_object()
        if article.author != request.user:
            return HttpResponseForbidden("You are not allowed to edit this article.")
        return super().dispatch(request, *args, **kwargs)


class ArticleDisplayView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        author_profile = Profile.objects.get(user=article.author)
        context['author_name'] = author_profile.username
        context['author_id'] = author_profile.user_id
        return context


def category_articles(request, category):
    if category not in CategoryChoices.values:
        # Handle invalid category (e.g., return a 404 error or redirect)
        return redirect('home')

    # Fetch articles of the given category
    articles = Article.objects.filter(category=category, is_published=True).order_by('-published_at')

    # Paginate the articles (5 per page)
    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'articles/category_articles.html', context)
