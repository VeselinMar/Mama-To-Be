from django.urls import path

from mama_to_be.forum.views import ForumCategoryListView, TopicListView, TopicDetailView, \
    create_topic, CreateCommentView, DiscussionDetailView, like_comment, ReplyCommentView

urlpatterns = [
    path('', ForumCategoryListView.as_view(), name='category-list'),
    path('category/<slug:category_slug>/', TopicListView.as_view(), name='topic-list'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('discussion/<int:discussion_id>/add-comment/', CreateCommentView.as_view(), name='create-comment'),
    path('comment/<int:comment_id>/reply/', ReplyCommentView.as_view(), name='reply-comment'),
    path('comment/<int:comment_id>/like/', like_comment, name='like-comment'),
    path('create-topic/', create_topic, name='create-topic'),
    path('discussion/<int:pk>/', DiscussionDetailView.as_view(), name='discussion-detail'),
]
