from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin

from mama_to_be.forum.forms import TopicForm, CommentForm, CategoryForm, DiscussionForm
from mama_to_be.forum.models import Topic, Comment, Like, Category, Discussion


# Create your views here.


class ForumCategoryListView(ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['category_form'] = CategoryForm()

        # Prefetch topics for all categories
        context['categories'] = Category.objects.prefetch_related('topics').all()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('category-list')
        return self.get(request, *args, **kwargs)


class TopicListView(UserPassesTestMixin, ListView):
    model = Topic
    template_name = 'forum/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return Topic.objects.filter(category__slug=category_slug)

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

    def test_func(self):
        # Restrict form usage to specific groups
        return self.request.user.groups.filter(name__in=['Restricted Admin', 'Unrestricted Admin']).exists()


class TopicDetailView(FormMixin, DetailView):
    model = Topic
    template_name = "forum/topic_detail.html"
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


@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('forum-home')
    else:
        form = TopicForm()
    return render(request, 'forum/create_topic.html', {'form': form})


class DiscussionDetailView(DetailView):
    model = Discussion
    template_name = "forum/discussion_detail.html"
    context_object_name = "discussion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


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
