from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView

from mama_to_be.forum.forms import TopicForm, CommentForm, CategoryForm
from mama_to_be.forum.models import Topic, Comment, Like, Category


# Create your views here.


class ForumCategoryListView(ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['category_form'] = CategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('category-list')
        return self.get(request)


class TopicListView(ListView):
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


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(topic=self.object).order_by('-likes')
        return context

    def post(self, request, *args, **kwargs):
        topic = self.get_object()
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.topic = topic
                comment.save()
                return redirect('topic-detail', pk=topic.pk)
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


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/create_comment.html'

    def dispatch(self, request, *args, **kwargs):
        # Fetch the topic and optionally the parent comment
        self.topic = get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))
        self.parent_comment = None

        if 'parent_id' in self.kwargs:
            self.parent_comment = get_object_or_404(Comment, pk=self.kwargs.get('parent_id'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Associate the topic and parent comment if provided
        form.instance.topic = self.topic
        form.instance.parent = self.parent_comment
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the topic detail page
        return reverse('topic-detail', kwargs={'pk': self.topic.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        context['parent_comment'] = self.parent_comment
        return context


class LikeCommentView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        like, created = Like.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            like.delete()
            comment.likes -= 1
        else:
            comment.likes += 1
        comment.save()
        return redirect('topic-detail', pk=comment.topic.pk)
