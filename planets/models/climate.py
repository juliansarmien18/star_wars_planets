from django.db import models

from core.models import AuditModel


class Climate(AuditModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
