from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from mforum.models import BaseUUID7Model


class Category(BaseUUID7Model):
    name = models.CharField(
        _("Name"),
        max_length=255,
    )
    slug = models.SlugField(
        _("Slug"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        _("Description"),
        blank=True,
    )
    position = models.PositiveIntegerField(
        _("Position"),
        default=0,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("position", "name")

    def __str__(self) -> str:
        return self.name


class Topic(BaseUUID7Model):
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        related_name="topics",
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        related_name="topics",
        on_delete=models.PROTECT,
    )
    title = models.CharField(
        _("Title"),
        max_length=255,
    )
    slug = models.SlugField(
        _("Slug"),
        max_length=255,
        unique=True,
    )
    is_pinned = models.BooleanField(
        _("Pinned"),
        default=False,
    )
    is_closed = models.BooleanField(
        _("Closed"),
        default=False,
    )

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ("-is_pinned", "-created_at")

    def __str__(self) -> str:
        return self.title


class Post(BaseUUID7Model):
    topic = models.ForeignKey(
        Topic,
        verbose_name=_("Topic"),
        related_name="posts",
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        related_name="posts",
        on_delete=models.PROTECT,
    )
    body = models.TextField(
        _("Body"),
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"{self.author}: {self.body[:50]}"
