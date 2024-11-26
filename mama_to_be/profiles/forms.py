from django import forms
from django.contrib.auth.forms import UserCreationForm
from mama_to_be.profiles.models import AppUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ['email', 'password1', 'password2']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
