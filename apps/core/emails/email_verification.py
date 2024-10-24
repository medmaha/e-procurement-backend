import os
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string

from APP_COMPANY import APP_COMPANY
from apps.core.processors.multithreading import MultiThreading
from apps.accounts.models.account import Account


def send_verification_code(user: Account, code: str | int, expires_at: str | int):
    context = {
        "verification_code": code,
        "APP_COMPANY": APP_COMPANY,
        "full_name": user.full_name,
        "expires_at": expires_at,
    }
    template = render_to_string("core/email_verification.html", context=context)

    mailer(user.email, template)


def mailer(recipient, template):
    target = lambda: send_mail(
        subject="Verify your email",
        message="",
        from_email=f"{APP_COMPANY.get('name')} <{os.environ.get("EMAIL_HOST_USER")}>",
        recipient_list=[recipient],
        fail_silently=False,
        html_message=template,
    )
    MultiThreading(target=target)
