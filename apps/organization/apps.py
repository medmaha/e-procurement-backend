from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.organization"
    verbose_name = "My Organization"

    def ready(self) -> None:
        from . import signals

        return super().ready()
