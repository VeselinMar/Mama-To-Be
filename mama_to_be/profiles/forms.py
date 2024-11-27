from django import forms
from django.contrib.auth.forms import UserCreationForm
from mama_to_be.profiles.models import AppUser, Profile


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


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'profile_picture', 'description']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself'}),
        }
