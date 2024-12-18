from django.db import transaction
from django.core.management.base import BaseCommand


from apps.core.scripts.clear_migration_files import delete_migration_files
from apps.core.scripts.clear_pycache_files import delete_pycache_files


class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.core.management import execute_from_command_line

        # from scaffold.automation.main import automate_scaffold

        # from scaffold.automation.thresholds import generate_thresholds

        # delete_pycache_files()
        # delete_migration_files(delete_db=True)
        #
        # execute_from_command_line(["manage.py", "makemigrations"])
        # execute_from_command_line(["manage.py", "migrate"])

        # execute_from_command_line(["manage.py", "create_superuser"])
        with transaction.atomic():
            from apps.core.automation.groups import DefaultPermissionGroups

            DefaultPermissionGroups.create_if_not_exist()
            # execute_from_command_line(["manage.py", "loaddata", "org.json"])
            # execute_from_command_line(["manage.py", "loaddata", "suppliers.json"])

            # generate_thresholds()
            # automate_scaffold()
            pass

        print("\n\t\t OK 👍🚀👍 Scaffolding Completed! ✅🚀👍")
