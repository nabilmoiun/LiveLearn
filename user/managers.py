from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, full_name, password=None, *args, **kwargs):
        if not email:
            raise ValueError("Email must be set")
        if not full_name:
            raise ValueError("Fullname must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            **kwargs
        )
        user.set_password(password)
        user.save()

    def create_superuser(self, email, full_name, password=None, *args, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        return self._create_user(email=email, full_name=full_name, password=password, *args, **kwargs)
