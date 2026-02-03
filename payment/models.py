from django.db import models
from django.conf import settings

from common.models import BaseModel
from enrollment.models import Enrollment


class Payment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments', on_delete=models.PROTECT)
    enrollment = models.ForeignKey(Enrollment, related_name='payments', on_delete=models.PROTECT)
    month = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "payments"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-created_at']

    def __str__(self):
        return self.user.full_name


