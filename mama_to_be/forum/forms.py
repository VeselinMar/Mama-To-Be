from django import forms

from mama_to_be.forum.models import Topic, Comment, Category, Discussion


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category description'
            })
        }
        labels = {
            'name': 'Category Name',
            'description': 'Description'
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


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Insert comment', 'rows': 3}),
        }
        labels = {
            'content': 'Content',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Insert comment', 'rows': 3}),
        }
        labels = {
            'content': 'Content',
        }
