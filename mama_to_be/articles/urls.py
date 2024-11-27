from django.urls import path

from mama_to_be.articles.views import ArticleCreateView, ArticleDisplayView, ArticleEditView

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create-article'),
    path('<slug:slug>/', ArticleDisplayView.as_view(), name='article-detail'),
    path('<slug:slug>/edit', ArticleEditView.as_view(), name='article-edit')
]
