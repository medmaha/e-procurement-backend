from django.db import models

# TODO capitalize all choices


class ProcurementMethodChoices(models.TextChoices):
    SINGLE_SOURCING = "single_sourcing", "Single Sourcing"
    REQUEST_FOR_QUOTATION = "rfq", "Request For Quotations"
    RESTRICTED_TENDER = "restricted_tender", "Restricted Tender"
    INTERNATIONAL_TENDER = "international_tender", "International Tender"
    NOT_APPLIED = "not_applied", "Not Applied"
    REQUEST_FOR_QUOTATION_2 = "rfq 2", "Request For Quotations 2"


class MeasurementUnitChoices(models.TextChoices):
    UNITS = "units", "Units"
    PIECES = "pieces", "Pieces"
    METRES = "metres", "Metres"
    INCHES = "inches", "Inches"
    BUNDLES = "bundles", "Bundles"
    BYTES = "bytes", "Bytes"
    LITERS = "litres", "Litres"
    OTHER = "other", "Other"


class ApprovalChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class RFQLevelChoices(models.TextChoices):
    APPROVAL_LEVEL = "APPROVAL LEVEL", "Approval Level"
    PUBLISH_LEVEL = "PUBLISH LEVEL", "Publish Level"
    QUOTATION_LEVEL = "QUOTATION LEVEL", "Quotation Level"
    EVALUATION_LEVEL = "EVALUATION LEVEL", "Evaluation Level"
    CONTRACT_LEVEL = "CONTRACT LEVEL", "Contract Level"
    PURCHASE_ORDER_LEVEL = "PURCHASE ORDER LEVEL", "Purchase Order Level"
    INVOICE_LEVEL = "INVOICE LEVEL", "Invoice Level"


class PaymentTermsChoices(models.TextChoices):
    NET_30 = "net_30", "Net 30 Days"
    NET_60 = "net_60", "Net 60 Days"
    NET_90 = "net_90", "Net 90 Days"
    DUE_ON_RECEIPT = "due_on_receipt", "Due on Receipt"
    CUSTOM = "custom", "Custom"  # Example for a custom term
