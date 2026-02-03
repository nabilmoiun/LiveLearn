from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save()

    def create_superuser(self, email, password=None, *args, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        return self._create_user(email=email, password=password, *args, **kwargs)
