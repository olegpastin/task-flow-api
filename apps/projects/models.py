from django.db import models
from django.db.models import Manager

from apps.users.models import User


class Project(models.Model):
    """
    Represents a model that groups tasks and users.

    A project has an owner and multiple members.
    Only project members can access its data.
    """
    name = models.CharField(
        verbose_name='Name',
        max_length=150
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        verbose_name='Owner',
        to=User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    members = models.ManyToManyField(
        verbose_name='Members',
        to=User,
        related_name='member_projects',
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
        return self.name
