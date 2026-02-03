from django.db import models

from common.models import BaseModel


class Subject(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)

    class Meta:
        db_table = "subjects"
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name', ]

    def __str__(self):
        return self.name
