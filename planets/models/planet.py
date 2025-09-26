from django.db import models

from core.models import AuditModel

from .climate import Climate
from .terrain import Terrain


class Planet(AuditModel):
    name = models.CharField(max_length=100, unique=True)
    population = models.BigIntegerField(null=True, blank=True)
    climates = models.ManyToManyField(Climate, blank=True)
    terrains = models.ManyToManyField(Terrain, blank=True)

    def __str__(self):
        return self.name
