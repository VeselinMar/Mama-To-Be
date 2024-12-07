from django.urls import path

from mama_to_be.forum.views import ForumCategoryListView, TopicListView, TopicDetailView, \
    LikeCommentView, create_topic, CreateCommentView

urlpatterns = [
    path('', ForumCategoryListView.as_view(), name='category-list'),
    path('category/<slug:category_slug>/', TopicListView.as_view(), name='topic-list'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('topic/<int:topic_id>/comment/', CreateCommentView.as_view(), name='create-comment'),
    path('topic/<int:topic_id>/comment/<int:parent_id>/', CreateCommentView.as_view(), name='reply-comment'),
    path('topic/<int:pk>/like/<int:comment_id>/', LikeCommentView.as_view(), name='like-comment'),
    path('create-topic/', create_topic, name='create-topic'),
]