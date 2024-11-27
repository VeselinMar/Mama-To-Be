from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, DetailView

from mama_to_be.articles.models import Article
from mama_to_be.profiles.forms import RegisterForm, ProfileEditForm
from mama_to_be.profiles.models import Profile


# Create your views here.

class RegisterView(FormView):
    template_name = "profiles/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("edit")

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
    form_class = AuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('home')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        # Ensure the logged-in user can only edit their own profile
        return Profile.objects.get(user=self.request.user)


class ProfileDisplayView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Check if username is provided in the URL, else fetch the profile for the logged-in user
        username = self.kwargs.get('username', None)

        if username:
            # Fetch the Profile based on the username of the related User model
            return get_object_or_404(Profile, user__username=username)
        else:
            # If no username, get the profile of the logged-in user
            return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_object()
        user = profile.user

        # Get the last 3 published articles for this user
        published_articles = Article.objects.filter(author=user, is_published=True).order_by('-published_at')[:3]

        # Include unpublished articles if the profile belongs to the logged-in user
        unpublished_articles = None
        if user == self.request.user:
            unpublished_articles = Article.objects.filter(author=user, is_published=False)

        context['published_articles'] = published_articles
        context['unpublished_articles'] = unpublished_articles
        return context
