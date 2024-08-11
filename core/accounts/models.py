from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager that handles authentication and authorization requests for the given user account.
    """

    def create_user(self, username, password, **extra_fields):
        """Create a new user"""
        if not username:
            raise ValueError(_("username must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, email=None, **extra_fields):
        """Create a new superuser"""

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("staff user must have set is_staff=True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must have set is_superuser=True"))

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    is_active = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    objects = UserManager()
