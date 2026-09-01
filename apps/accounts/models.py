from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Project user identity, intentionally minimal in the technical foundation."""

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
