from django.urls import path

from .views.account import LoginAPIView

from .views.groups.get import GroupGetAPIView
from .views.groups.put import GroupUpdateAPIView
from .views.groups.list import GroupListAPIView
from .views.groups.post import GroupCreateAPIView
from .views.groups.query import GroupQueryAPIView
from .views.groups.delete import GroupDisableAPIView


# reference --> /api/auth/*
urlpatterns = [
    # Authentication
    path("login/", LoginAPIView.as_view()),
    # Auth Groups
    path("groups/", GroupListAPIView.as_view()),
    path("groups/query/", GroupQueryAPIView.as_view()),
    path("groups/create/", GroupCreateAPIView.as_view()),
    path("groups/<group_id>/", GroupGetAPIView.as_view()),
    path("groups/<group_id>/update/", GroupUpdateAPIView.as_view()),
    path("groups/<group_id>/disable/", GroupDisableAPIView.as_view()),
]
