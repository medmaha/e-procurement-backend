from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Organization Auth Management"

    def ready(self) -> None:
        from . import signal

        return super().ready()
