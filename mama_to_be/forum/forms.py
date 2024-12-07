from django import forms

from mama_to_be.forum.models import Topic, Comment, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
        }
        labels = {
            'name': 'Category Name',
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter topic title'}),
        }
        labels = {
            'title': 'Title',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
