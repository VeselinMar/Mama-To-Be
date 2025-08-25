from django import forms
from django.forms import inlineformset_factory

from mama_to_be.common.models import ToDoList, Task


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ["title", "is_editable_by_shared_users"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter list title"}),
            "is_editable_by_shared_users": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    TaskFormSet = inlineformset_factory(
        ToDoList,
        Task,
        fields=["text"],
        extra=1,
        widgets={
            "text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter task"})
    })