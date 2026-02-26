from django.urls import path

from mama_to_be.articles.views import (ArticleCreateView, ArticleDisplayView,
                                       ArticleEditView, CategoryArticlesView, search_view,
                                       RecentArticlesView, upload_image)

app_name = "articles"

urlpatterns = [
    path('', RecentArticlesView.as_view(), name='recent-articles'),
    path('create/', ArticleCreateView.as_view(), name='create-article'),
    path('search/', search_view, name='search'),
    path('upload-image/', upload_image, name='upload-image'),
    path('<slug:slug>/', ArticleDisplayView.as_view(), name='article-detail'),
    path('<slug:slug>/edit', ArticleEditView.as_view(), name='article-edit'),
    path('category/<str:category>/', CategoryArticlesView.as_view(), name='category-articles'),
    
    # TinyMce image upload endpoint
]
