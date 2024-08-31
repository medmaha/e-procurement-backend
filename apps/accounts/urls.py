from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.account, name="account"),
    path("login/", views.login_account, name="account_login"),
    path("logout/", views.logout_account, name="account_logout"),
    path("signup/", views.signup_account, name="account_signup"),
    path("signup/vendor", views.vendor_signup, name="vendor_signup"),
    path(
        "signup/vendor/complete", views.vendor_signup_complete, name="vendor_completion"
    ),
    path(
        "signup/vendor/activate",
        views.vendor_activate_await,
        name="vendor_activation_await",
    ),
    path(
        "signup/vendor/activate/process",
        views.vendor_activate,
        name="vendor_activation_proceed",
    ),
    path(
        "signup/vendor/activate/logout",
        views.logout_verification,
        name="logout_verification",
    ),
    path("signup/vendor/cancellation/", views.cancel_signup, name="signup_cancel"),
]
