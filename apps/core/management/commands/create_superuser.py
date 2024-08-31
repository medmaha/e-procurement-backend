import os
from apps.accounts.models import Account
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = os.getenv("SUPERUSER_EMAIL")
        password = os.getenv("SUPERUSER_PASSWORD")

        if not email or not password:
            raise ValueError("Email and password are required to create a superuser")

        exists = Account.objects.filter(email=email).exists()

        print("\nCreating Superuser Account")
        if exists:
            return
        account = Account(
            email=email,
            is_superuser=True,
            is_active=True,
            is_staff=True,
            first_name=os.getenv("SUPERUSER_FIRST_NAME") or "Admin",
            last_name=os.getenv("SUPERUSER_LAST_NAME") or "User",
            middle_name=os.getenv("SUPERUSER_MIDDLE_NAME") or "",
        )
        account.set_password(password)
        account.save()
        print("Superuser Created [%s]" % account.full_name)


messages = [
    "An quotation was submitted by IntraSoft Ltds",
    "Your Requisition was rejected by the procurement department",
    "A new bid has been placed on your request",
    "An order has been processed for delivery",
    "Your invoice has been approved for payment",
    "Supplier XYZ has updated their catalog",
    "You have been assigned as the approver for a purchase request",
    "A contract renewal is due next week",
    "A vendor has updated their terms and conditions",
    "A new procurement policy has been published",
]

pages_url = [
    None,
    "/procurement/requisitions?view=4",
    None,
    "/procurement/purchase-orders/create?quotation=2",
    None,
    "/procurement/invoices",
    None,
]
