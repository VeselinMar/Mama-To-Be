from django.urls import path

from mama_to_be.forum.views import (ForumCategoryListView, TopicListView, TopicDetailView,
                                    CreateCommentView, DiscussionDetailView, like_comment,
                                    ReplyCommentView, CategoryUpdateView,
                                    TopicEditView, EditCommentView, EditDiscussionView)

urlpatterns = [
    path('', ForumCategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('category/<slug:category_slug>/', TopicListView.as_view(), name='topic-list'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('topic/<int:pk>/edit/', TopicEditView.as_view(), name='topic-edit'),
    path('discussion/<int:pk>/', DiscussionDetailView.as_view(), name='discussion-detail'),
    path('discussion/<int:discussion_id>/add-comment/', CreateCommentView.as_view(), name='create-comment'),
    path('discussion/<int:pk>/edit/', EditDiscussionView.as_view(), name='edit-discussion'),
    path('comment/<int:comment_id>/reply/', ReplyCommentView.as_view(), name='reply-comment'),
    path('comment/<int:pk>/edit/', EditCommentView.as_view(), name='edit-comment'),
    path('comment/<int:comment_id>/like/', like_comment, name='like-comment'),
]
