from django.db import models
from django.conf import settings

from teacher.models import Batch
from common.models import BaseModel


class Enrollment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, related_name='enrollments', on_delete=models.PROTECT)
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2)
    admission_fee = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "enrollments"
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        ordering = ['-created_at']
        unique_together = (
            ("user", "batch", )
        )

    def __str__(self):
        return self.user.full_name


