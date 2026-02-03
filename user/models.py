from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from common.models import BaseModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'

    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.STUDENT)
    avatar = models.ImageField(upload_to="user_avatars", null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = UserManager()

    REQUIRED_FIELDS = ["full_name", ]
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def __str__(self):
        return self.email
