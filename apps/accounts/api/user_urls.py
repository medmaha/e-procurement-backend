from django.urls import path

# Accounts
from .views.users.list import AccountListView
from .views.users.get import AccountGetView
from .views.users.put import AccountUpdateView
from .views.users.post import AccountCreateView
from .views.users.query import AccountQueryView
from .views.users.delete import AccountDisableAPIView

# reference --> /api/users/*
urlpatterns = [
    path("", AccountListView.as_view()),
    path("query/", AccountQueryView.as_view()),
    path("create/", AccountCreateView.as_view()),
    path("<str:user_id>/", AccountGetView.as_view()),
    path("<str:user_id>/update/", AccountUpdateView.as_view()),
    path("<str:user_id>/disable/", AccountDisableAPIView.as_view()),
]
