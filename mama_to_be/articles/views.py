from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView

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

        return super().form_valid(form)


class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to edit an existing article. Only accessible to author.
    """
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article_form.html'
    context_object_name = 'article'

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'slug': self.object.slug})


class ArticleDisplayView(DetailView):
    """
    View to display an article. Freely accessible.
    """
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


class CategoryArticlesView(ListView):
    model = Article
    template_name = 'articles/category_articles.html'
    context_object_name = 'object_list'  # Default name for the queryset
    paginate_by = 9

    def get_queryset(self):
        # Validate the category from the URL
        category = self.kwargs.get('category')
        if category not in CategoryChoices.values:
            raise Http404("Invalid category")  # Return 404 for invalid category

        # Use the custom manager's `in_category` method to fetch published articles in this category
        return Article.objects.in_category(category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the category to the context for use in the template
        context['category'] = self.kwargs['category']
        # Ensure page_obj is explicitly passed to the context
        context['page_obj'] = context.get('page_obj', context['object_list'])
        return context
