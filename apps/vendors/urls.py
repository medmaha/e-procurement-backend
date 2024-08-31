from django.urls import path

from . import views

urlpatterns = [
    path("quotations/", views.quotation_list, name="quotations"),
    path("quotations/<id>", views.quotation_detail, name="quotation_detail"),
    path("quotations/<id>/accept/", views.quotation_accept, name="quotation_accept"),
    path("quotations/<id>/reject/", views.quotation_reject, name="quotation_reject"),
]
