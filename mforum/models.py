from uuid import UUID

import uuid_utils
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseTimestampModel(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    class Meta:
        abstract = True


class BaseModel(BaseTimestampModel):
    class Meta:
        abstract = True


def _uuid7() -> UUID:
    return UUID(str(uuid_utils.uuid7()))


class BaseUUID7Model(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=_uuid7,
        editable=False,
    )

    class Meta:
        abstract = True
