from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from mama_to_be.profiles.forms import RegisterForm


# Create your views here.

class RegisterView(FormView):
    template_name = "profiles/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

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
