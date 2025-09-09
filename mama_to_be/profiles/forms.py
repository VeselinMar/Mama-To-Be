from django import forms
from django.contrib.auth.forms import AuthenticationForm
from mama_to_be.profiles.models import AppUser, Profile


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ['email']

    def clean_password2(self):
        email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

        if password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'profile_picture', 'description']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself'}),
        }
