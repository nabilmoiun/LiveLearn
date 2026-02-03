import uuid
from django.db import models


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
