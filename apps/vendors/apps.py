from django.apps import AppConfig


class VendorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.vendors"
    verbose_name = "Suppliers"

    def ready(self) -> None:
        from . import signals

        return super().ready()
