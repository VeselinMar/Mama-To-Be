from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, DetailView

from mama_to_be.articles.models import Article
from mama_to_be.profiles.forms import RegisterForm, ProfileEditForm, CustomLoginForm
from mama_to_be.profiles.models import Profile


# Create your views here.

class RegisterView(FormView):
    template_name = "profiles/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("profile-edit")

    def form_valid(self, form):
        # Save the user and log them in
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your registration. Please try again.")
        return super().form_invalid(form)


class CustomLoginView(FormView):
    template_name = 'profiles/login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('home')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('home')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'profiles/profile_update.html'

    def get_object(self, queryset=None):
        # Return the current user's profile efficiently
        return self.request.user.profile

    def get_success_url(self):
        # Redirect to the profile display page of the current user after editing
        return reverse_lazy('profile-display', kwargs={'user_id': self.request.user.id})


class ProfileDisplayView(DetailView):
    model = Profile
    template_name = 'profiles/profile_details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Use the user_id parameter, if provided, or default to the logged-in user's profile
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            return get_object_or_404(Profile, user__id=user_id)
        return self.request.user.profile  # Default to the logged-in user's profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the profile object
        profile = self.get_object()
        user = profile.user

        # Fetch the last 3 published articles for this user
        published_articles = Article.objects.filter(author=user, is_published=True).order_by('-published_at')[:3]

        # Include unpublished articles only if the profile belongs to the logged-in user
        unpublished_articles = None
        if user == self.request.user:
            unpublished_articles = Article.objects.filter(author=user, is_published=False)

        context['published_articles'] = published_articles
        context['unpublished_articles'] = unpublished_articles
        return context
