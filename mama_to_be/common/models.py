from django.db import models

from mama_to_be import settings
from mama_to_be.common.choices import PriorityChoices


# Create your models here.

# To Do List

class ToDoList(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="todo_lists"
        )

    title = models.CharField(
        max_length=255,
    )

    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="shared_todo_lists",
        blank=True,
    )

    is_editable_by_shared_users = models.BooleanField(
        default=False,
    )

    def can_add_more_lists(self):
        """Checks if user has already created maximum number of lists. """
        if self.owner:
            return self.owner.todo_lists.count() < 3
        return False

    def __str__(self):
        return self.title


class Task(models.Model):
    todo_list = models.ForeignKey(
        ToDoList,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    description = models.CharField(
        max_length=500,
    )

    is_completed = models.BooleanField(
        default=False,
    )

    priority = models.CharField(
        max_length=10,
        choices = PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.description
