from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.health_check.models import TimeStampedModel
from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    class Meta:
        db_table = 'auth_users'

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()


class ProfileModel(models.Model):
    class Meta:
        db_table = 'profile'

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.IntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
