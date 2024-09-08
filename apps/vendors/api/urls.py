from django.urls import path


#
from .views.list import VendorSelectView

#
from .views.rfq_response.list import RFQResponseListView
from .views.rfq_response.submit import RFQSubmitView
from .views.rfq_response.retrieve import RFQResponseGetAPIView

#
from .views.rfq_request.list import RFQRequestListView

#
from .views.contact_person.list import ContactPersonListView
from .views.contact_person.update import ContactPersonUpdateView
from .views.contact_person.verify import ContactPersonVerifyView
from .views.contact_person.retrieve import (
    ContactPersonGetAPIView,
    ContactPersonRetrieveDetailsView,
)

#
from .views.certificates.list import CertificationListView
from .views.certificates.create import CertificationCreateView
from .views.certificates.update import CertificationUpdateView
from .views.certificates.retrieve import CertificateGetAPIView
from .views.certificates.verification import CertificationVerificationUpdateView

#
from .views.registration.list import RegistrationListView
from .views.registration.update import RegistrationUpdateView
from .views.registration.activation import VendorActivationUpdateView
from .views.registration.retrieve import VendorRegistrationGetAPIView

#
from .views.invoices.list import InvoiceListView

#
from .views.rfq_contracts.list import RFQContractListView
from .views.rfq_contracts.negotiations import RFQContractNegotiationView

#
from .views.vendors.list import VendorListView
from .views.vendors.retrieve import VendorGetAPIView, VendorDetailsView


# reference -> /api/vendors/*
urlpatterns = [
    path("select/", VendorSelectView.as_view()),
    #
    # if request.user is Vendor retrieve the Vendor instance
    #  request.user must include a id query param to retrieve a Vendor
    path("retrieve/", VendorGetAPIView.as_view()),
    #
    path("rfq-responses/submit/", RFQSubmitView.as_view()),
    path("rfq-responses/<id>/", RFQResponseGetAPIView.as_view()),
    path("rfq-responses/", RFQResponseListView.as_view()),
    path("rfq/<id>/", RFQResponseGetAPIView.as_view()),
    path("rfq/", RFQResponseListView.as_view()),
    path("rfq-responses/submit/", RFQSubmitView.as_view()),
    #
    path("rfq-requests/<id>/", RFQResponseGetAPIView.as_view()),
    path("rfq-requests/", RFQRequestListView.as_view()),
    path("rfq/<id>/", RFQResponseGetAPIView.as_view()),
    #
    path("contracts/negotiations/list/", RFQContractNegotiationView.as_view()),
    path("contracts/negotiations/<contract_id>/", RFQContractNegotiationView.as_view()),
    path("contracts/negotiations/", RFQContractNegotiationView.as_view()),
    #
    path("contracts/list/", RFQContractListView.as_view()),
    path("contracts/<id>/", RFQContractListView.as_view()),
    path("contracts/", RFQContractListView.as_view()),
    #
    path("contact-person/retrieve/", ContactPersonGetAPIView.as_view()),
    path("contact-person/update/", ContactPersonUpdateView.as_view()),
    path("contact-person/verify/", ContactPersonVerifyView.as_view()),
    path("contact-person/list/", ContactPersonListView.as_view()),
    path("contact-person/<slug>/", ContactPersonRetrieveDetailsView.as_view()),
    path("contact-person/", ContactPersonListView.as_view()),
    path("rfq/", RFQResponseListView.as_view()),
    #
    path("certificates/create/", CertificationCreateView.as_view()),
    path("certificates/update/", CertificationUpdateView.as_view()),
    path("certificates/verification/", CertificationVerificationUpdateView.as_view()),
    path("certificates/list/", CertificationListView.as_view()),
    path("certificates/<slug>/", CertificateGetAPIView.as_view()),
    path("certificates/", CertificationListView.as_view()),
    #
    path("invoices/", InvoiceListView.as_view()),
    #
    path("registration/update/", RegistrationUpdateView.as_view()),
    path("registration/activation/", VendorActivationUpdateView.as_view()),
    path("registration/list", RegistrationListView.as_view()),
    path("registration/<slug>/", VendorRegistrationGetAPIView.as_view()),
    path("registration/", RegistrationListView.as_view()),
    #
    # Route is meant for staff members not for vendors
    path("", VendorListView.as_view()),
    path("retrieve/", VendorGetAPIView.as_view()),
    path("<slug>/", VendorDetailsView.as_view()),
]
