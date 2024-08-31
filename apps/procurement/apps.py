from django.apps import AppConfig


class ProcurementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.procurement"

    def ready(self) -> None:
        from . import signals

        return super().ready()
