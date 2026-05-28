from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Your name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your email"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Your message",
            "rows": 6
        })
    )

    # Honeypot
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return cleaned_data