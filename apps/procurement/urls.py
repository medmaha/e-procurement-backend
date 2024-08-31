from django.urls import path
from . import views


# reference /procurement/*
urlpatterns = [
    # path(
    #     "requisitions/accepted",
    #     views.requisitions_accepted,
    #     name="requisitions_accepted",
    # ),
    # path(
    #     "requisitions/rejected",
    #     views.requisitions_rejected,
    #     name="requisitions_rejected",
    # ),
    # path(
    #     "requisitions/pending", views.requisitions_pending, name="requisitions_pending"
    # ),
    # path("requisitions/all", views.requisitions_all, name="requisitions_all"),
    # path("rfq", views.rfq, name="rfq"),
    # path("rfq/detail/<id>/", views.rfq_detail, name="rfq_detail"),
    # path("tender", views.tender, name="tender"),
    # path("single-sourcing", views.single_source, name="single_source"),
    # path("", views.procurement_view, name="procurement"),
    # path("method", views.procurement_method, name="procurement_method"),
]


from .views.requisitions.urls import requisitions_url

urlpatterns += requisitions_url
