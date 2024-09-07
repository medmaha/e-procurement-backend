from django.urls import path

from . import views

# Groups
from .views.groups.create import GroupCreateView
from .views.groups.update import GroupUpdateView
from .views.groups.list import (
    GroupListView,
    GroupListSelectView,
)

# Permissions
from .views.permissions.list import (
    PermissionSelectListView,
)

# Accounts
from .views.account.list import AccountListView
from .views.account.retrieve import AccountRetrieveView

# reference --> /api/account/*
urlpatterns = [
    #
    # Accounts
    # path("users/", AccountListView.as_view()),
    # path("users/<user_id>/", AccountRetrieveView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("signup/", views.VendorSignupView.as_view()),
    # path("session/", views.RefreshAuthSessionTokens.as_view()),
    #
    # Groups
    # path("groups/create/", GroupCreateView.as_view()),
    # path("groups/update/", GroupUpdateView.as_view()),
    # path("groups/select/", GroupListSelectView.as_view()),
    # path("groups/", GroupListView.as_view()),
    #
    # Permissions
    # path("permissions/select/", PermissionSelectListView.as_view()),
]
