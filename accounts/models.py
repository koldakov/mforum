from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from mforum.models import BaseUUID7Model


class User(BaseUUID7Model, AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
