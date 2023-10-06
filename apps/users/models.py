from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.health_check.models import TimeStampedModel
from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Custom user model representing user in the system."""

    class Meta:
        db_table = 'auth_users'
        ordering = ('-created_at',)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name']


class ProfileModel(models.Model):
    """Custom profile model representing user profile in the system."""

    class Meta:
        db_table = 'profile'

    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    age = models.IntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
