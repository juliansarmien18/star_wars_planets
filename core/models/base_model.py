from django.db import models
from django.utils.timezone import now
from django_currentuser.db.models import CurrentUserField


class AuditModel(models.Model):
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)
    created_by = CurrentUserField(
        on_update=False,
        related_name="created_%(class)ss",
        related_query_name="created_%(class)s",
    )
    updated_by = CurrentUserField(
        on_update=True,
        related_name="updated_%(class)ss",
        related_query_name="updated_%(class)s",
    )

    class Meta:
        abstract = True
