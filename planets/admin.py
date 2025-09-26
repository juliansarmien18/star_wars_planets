from django.contrib import admin
from django.db import models

from . import models as planets_models

AUDIT_FIELDS = {"created_at", "updated_at", "created_by", "updated_by"}


def register_model_admin(model):
    model_fields = [f.name for f in model._meta.fields]
    search = ["name"] if "name" in model_fields else []
    exclude = [f for f in model_fields if f in AUDIT_FIELDS]

    attrs = {
        "exclude": exclude,
        "search_fields": search,
    }

    admin_class = type(f"{model.__name__}Admin", (admin.ModelAdmin,), attrs)

    if not admin.site.is_registered(model):
        admin.site.register(model, admin_class)


for model_name in getattr(planets_models, "__all__", []):
    model_class = getattr(planets_models, model_name, None)
    if (
        isinstance(model_class, type)
        and issubclass(model_class, models.Model)
        and not model_class._meta.abstract
    ):
        register_model_admin(model_class)
