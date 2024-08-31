import re
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from apps.accounts.models import Account
from apps.core.decorators.permissions import staff_view
from apps.procurement.models.requisition import Requisition
from apps.procurement.models.requisition_approval import RequisitionApproval
from apps.vendors.models import Vendor
from backend.apps.vendors.models.rfq_response import Quotation


@login_required
def index(request: HttpRequest):
    context = {"active_tab": "home"}
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))
    return render(request, "core/email_verification.html", context=context)


@login_required
def dashboard(request: HttpRequest):
    welcome = request.GET.get("welcome")
    user: Account = request.user  # type: ignore
    welcome_text = None

    context = {}

    if welcome:
        welcome_text = (
            f"Welcome {user.first_name.capitalize()} {user.last_name.capitalize()}"
        )

    profile_name = user.get_profile()[0].lower()
    profile_instance = user.get_profile()[1]

    if profile_name == "staff":
        requisitions = Requisition.objects.filter(staff=profile_instance)
        requisition_approvals = RequisitionApproval.objects.filter(
            requisition__in=requisitions
        )
        context["staff"] = profile_instance
        context["requisitions"] = requisitions
        context["requisition_approvals"] = requisition_approvals

    elif profile_name == "vendor":
        context["vendor"] = profile_instance
        context["products_data"] = [
            {
                "product_id": 1,
                "name": "Product X",
                "description": "Description of Product X",
                "price": 50.00,
                "quantity_available": 100,
            },
            {
                "product_id": 2,
                "name": "Product Y",
                "description": "Description of Product Y",
                "price": 75.00,
                "quantity_available": 50,
            },
            # Add more dummy product data as needed
        ]
        context["messages_data"] = [
            {
                "sender": "Admin",
                "subject": "Important Update",
                "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "date": "2023-11-20",
                "is_read": False,
            },
            {
                "sender": "System",
                "subject": "New Feature Announcement",
                "message": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "date": "2023-11-18",
                "is_read": True,
            },
            # Add more message data as needed
        ]

        context["tenders_data"] = [
            {
                "tender_id": "T2001",
                "title": "Tender for Supply of Goods",
                "deadline": "2023-12-15",
            },
            # Add more tender data as needed
        ]
        context["quotations_received"] = Quotation.objects.filter(
            vendor=user.profile
        ).order_by("-last_modified", "-created_date")[:3]
        context["quotations_response"] = Quotation.objects.filter(vendor=user.profile)

        context["analytics_data"] = {
            "total_orders": 150,
            "total_revenue": 25000.00,
            "top_product": "Product X",
            "top_product_sales": 75,
            # Add more analytics data as needed
        }
        context["orders_data"] = [
            {
                "order_id": 1,
                "customer": "Company A",
                "order_date": "2023-11-10",
                "total_amount": 1500.00,
                "status": "Pending",
            },
            {
                "order_id": 2,
                "customer": "Company B",
                "order_date": "2023-11-15",
                "total_amount": 2500.00,
                "status": "Processing",
            },
            # Add more dummy order data as needed
        ]

    context.update(
        {
            "active_tab": "home",
            "info_message": welcome_text,
        }
    )
    return render(
        request,
        "dashboard/dashboard.html",
        context=context,
        status=201 if welcome_text else 200,
    )


@login_required
def procurement(request: HttpRequest):
    return render(request, "dashboard/procurement.html")
