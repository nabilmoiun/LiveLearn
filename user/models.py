import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampModel):
    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STUDENT = 'student', 'Student'
        INSTRUCTOR = 'instructor', 'Instructor'

    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.STUDENT)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def __str__(self):
        return self.email
