from django.urls import path

from .company.get import CompanyRetrieveAPIView
from .company.put import CompanyUpdateAPIView
from .company.list import CompanyListAPIView
from .company.query import CompanyQueryAPIView
from .company.post import CompanyCreateAPIView
from .company.delete import CompanyDeleteAPIView


company_urlpatterns = [
    path("", CompanyListAPIView.as_view()),
    path("query/", CompanyQueryAPIView.as_view()),
    path("create/", CompanyCreateAPIView.as_view()),
    path("<slug>/", CompanyRetrieveAPIView.as_view()),
    path("<slug>/update/", CompanyUpdateAPIView.as_view()),
    path("<slug>/delete/", CompanyDeleteAPIView.as_view()),
]


urlpatterns = [*company_urlpatterns]
