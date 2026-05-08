from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Represents a custom user model that uses email as the authentication identifier."""
    objects = CustomUserManager()

    email = models.EmailField(
        verbose_name='E-Mail',
        unique=True,
        db_index=True
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=100,
        unique=True,
        db_index=True
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=50,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=50,
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(
        verbose_name='Date joined',
        auto_now_add=True
    )

    is_active = models.BooleanField(
        verbose_name='Is active?',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='Is staff?',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'username',

    def __str__(self):
        return self.username
