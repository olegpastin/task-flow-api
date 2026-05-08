from django.db import models
from django.db.models import Manager

from apps.projects.models import Project
from apps.users.models import User


class TaskStatus(models.TextChoices):
    """Available status values for tasks."""
    TODO = 'todo', 'Todo'
    IN_PROGRESS = 'in_progress', 'In progress'
    DONE = 'done', 'Done'


class TaskPriorities(models.TextChoices):
    """Available priority levels for tasks."""
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'


class Task(models.Model):
    """
    Represents a task within a project with status, priority and assignment.
    """
    project = models.ForeignKey(
        verbose_name='Project',
        to=Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(
        verbose_name='Title',
        max_length=150
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    priority = models.CharField(
        verbose_name='Priority',
        max_length=20,
        choices=TaskPriorities.choices,
        default=TaskPriorities.LOW
    )
    assignee = models.ForeignKey(
        verbose_name='Assignee',
        to=User,
        on_delete=models.PROTECT,
        related_name='assignee_tasks',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        verbose_name='Created by',
        to=User,
        on_delete=models.CASCADE,
        related_name='user_tasks'
    )
    due_date = models.DateField(
        verbose_name='Due date (deadline)',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['due_date']),
        ]


class Comment(models.Model):
    """Represents a comment made by a project member on a task."""
    task = models.ForeignKey(
        verbose_name='Task',
        to=Task,
        on_delete=models.CASCADE,
        related_name='task_comments'
    )
    author = models.ForeignKey(
        verbose_name='Author',
        to=User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    text = models.TextField(
        verbose_name='Text'
    )

    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        auto_now=True
    )

    def __str__(self):
        return self.text[:50]
