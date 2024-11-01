import typing
import apps.procurement.models as proc
import apps.organization.models as org

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.core.constants import DefaultGroups


class DefaultPermissionGroups(DefaultGroups):

    @classmethod
    def bootstrap_groups_dict(cls) -> dict[str, typing.Any]:

        bootstrapped = cls.bootstrap_groups()

        data = {}
        for group in bootstrapped:
            data[group["name"]] = group["perms"]

        return data

    @classmethod
    def create_if_not_exist(cls):
        bootstrapped = cls.bootstrap_groups()
        for group in bootstrapped:
            _group, _ = Group.objects.get_or_create(name=group["name"])
            cleaned = False
            for perm in group["perms"]:
                app_label, codename = perm.split(".")
                model_name: str = codename.split("_")[1]

                contenttype = ContentType.objects.get(
                    app_label=app_label, model__iexact=model_name
                )

                if not cleaned:
                    # Delete all existing
                    Permission.objects.filter(
                        codename=codename,
                        content_type=contenttype,
                    ).delete()

                    Permission.objects.filter(content_type=contenttype).delete()
                    cleaned = True

                model: str = codename.replace("_", " ").capitalize()
                permission, _ = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=contenttype,
                    name=(f"Can {model}"),
                )

                _group.permissions.add(permission)
