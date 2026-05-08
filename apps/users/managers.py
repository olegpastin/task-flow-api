from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """Manager for creating regular users and superusers."""
    def validate_user(self, email, username, password):
        """Validate required fields for user creation."""
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise ValueError('Incorrect E-Mail.')
        else:
            raise ValueError('E-Mail is required.')

        if not username:
            raise ValueError('Username is required.')
        if not password:
            raise ValueError('Password is required.')

    def create_user(self, email, username, password, **extra_fields):
        """Create and return a regular user with a hashed password."""
        email = self.normalize_email(email)
        self.validate_user(email, username, password)

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def validate_superuser(self, **extra_fields):
        """Validate required flags for superuser creation."""
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff flag is required for superuser.')

        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_active') is not True:
            raise ValueError('is_active flag is required for superuser.')

        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser flag is required for superuser.')

        return extra_fields

    def create_superuser(self, email, username, password, **extra_fields):
        """Create and return a superuser with required permission flags."""
        self.validate_superuser(**extra_fields)
        user = self.create_user(email, username, password, **extra_fields)
        return user
