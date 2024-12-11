from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import now

from mama_to_be.profiles.managers import AppUserManager


# Create your models here.


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Email Address"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        default=now,
        verbose_name="Date Joined"
    )

    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Last Login"
    )

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    username = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Username',
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name='Profile Picture',
        default='profile_pictures/381A0560.jpg'
    )

    description = models.TextField(
        blank=True,
        null=True,
        max_length=250,
    )

    def __str__(self):
        if self.username:
            return f"Profile of {self.username}"
        else:
            return f"Profile of {self.user.email}"
