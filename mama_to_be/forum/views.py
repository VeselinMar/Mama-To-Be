from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import BooleanField, Value, F, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from mama_to_be.forum.forms import TopicForm, CommentForm, CategoryForm, DiscussionForm
from mama_to_be.forum.models import Topic, Comment, Like, Category, Discussion
from mama_to_be.settings import ADMIN_GROUPS


# Create your views here.


# Category Views
class ForumCategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'forum/categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is an admin
        is_admin = self.request.user.groups.filter(name__in=ADMIN_GROUPS).exists()
        context['is_admin'] = is_admin

        # Add the category form if the user is an admin
        if is_admin:
            context['category_form'] = CategoryForm(user=self.request.user)
        return context

    def get_queryset(self):
        # Prefetch related topics to minimize database hits
        return Category.objects.prefetch_related(
            Prefetch('topics', queryset=Topic.objects.only('title', 'created_by', 'created_at'))
        )

    def post(self, request, *args, **kwargs):
        # Only admins can create new categories
        if request.user.groups.filter(name__in=ADMIN_GROUPS).exists():
            form = CategoryForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('category-list')
        return self.get(request, *args, **kwargs)


class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'forum/categories/category_edit.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        # Restrict access to specific groups
        return self.request.user.groups.filter(
            name__in=ADMIN_GROUPS
        ).exists()


# Topic Views
class TopicListView(ListView):
    model = Topic
    template_name = 'forum/topics/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 5

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        topics = Topic.objects.filter(category__slug=category_slug)
        user = self.request.user

        if user.is_authenticated:
            is_admin = user.groups.filter(name__in=ADMIN_GROUPS).exists()
            # Annotate each topic with an "is_editable" field
            topics = topics.annotate(
                is_editable=Value(
                    is_admin or (user == F('created_by')),
                    output_field=BooleanField()
                )
            )
        return topics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = Category.objects.get(slug=category_slug)
        context['topic_form'] = TopicForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            category_slug = self.kwargs.get('category_slug')
            category = Category.objects.get(slug=category_slug)
            form = TopicForm(request.POST)

            if form.is_valid():
                topic = form.save(commit=False)
                topic.category = category
                topic.created_by = request.user
                topic.save()
                return redirect(reverse('topic-list', kwargs={'category_slug': category_slug}))

        return self.get(request, *args, **kwargs)


class TopicDetailView(FormMixin, DetailView):
    model = Topic
    template_name = "forum/topics/topic_detail.html"
    context_object_name = "topic"
    form_class = DiscussionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.object
        context['discussions'] = topic.discussions.all()
        context['discussion_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            topic = self.get_object()
            discussion = form.save(commit=False)
            discussion.topic = topic
            discussion.created_by = request.user
            discussion.save()
            return self.get(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)


class TopicEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "forum/topics/topic_edit.html"
    context_object_name = "topic"

    def test_func(self):
        # Get the topic instance
        topic = self.get_object()
        # Check if the user is the author or belongs to one of the admin groups
        return (
            self.request.user == topic.created_by or
            self.request.user.groups.filter(name__in=['Restricted Admin', 'Unrestricted Admin']).exists()
        )

    def get_success_url(self):
        # Redirect to the topic detail page after successful editing
        return reverse('category-list')


# Discussion views
class DiscussionDetailView(DetailView):
    model = Discussion
    template_name = "forum/discussions/discussion_detail.html"
    context_object_name = "discussion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class EditDiscussionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Discussion
    fields = ['content']
    template_name = "forum/discussions/discussion_edit.html"

    def test_func(self):
        """Ensure the user is the author of the discussion."""
        discussion = self.get_object()
        return self.request.user == discussion.created_by

    def get_success_url(self):
        """Redirect back to the topic detail page."""
        return reverse('topic-detail', kwargs={'pk': self.object.topic.pk})


# Comment Views
class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        discussion_id = self.kwargs.get('discussion_id')
        self.discussion = get_object_or_404(Discussion, pk=discussion_id)
        form.instance.discussion = self.discussion
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('discussion-detail', kwargs={'pk': self.discussion.pk})


class ReplyCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.parent_comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        self.discussion = self.parent_comment.discussion  # Get the discussion of the parent comment
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.parent = self.parent_comment  # Link the parent comment
        form.instance.discussion = self.discussion  # Ensure the reply is linked to the same discussion
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('discussion-detail', kwargs={'pk': self.discussion.pk})


class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "forum/comments/comment_edit.html"

    def test_func(self):
        """Ensure that only the comment's creator can edit it."""
        comment = self.get_object()
        return comment.created_by == self.request.user

    def get_success_url(self):
        return reverse('discussion-detail', kwargs={'pk': self.object.discussion.pk})


# Others
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user already liked the comment
    like, created = Like.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        # User already liked, so remove the like
        like.delete()
        comment.likes -= 1  # Decrease like count
    else:
        # New like, add it
        comment.likes += 1  # Increase like count

    comment.save()

    # Return updated like count as JSON
    return JsonResponse({'likes': comment.likes})
