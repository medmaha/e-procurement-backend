from django.contrib import admin

from ..models import RFQContract, RFQNegotiation, RFQNegotiationNote, RFQContractAward


@admin.register(RFQContract)
class RFQContractAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "rfq",
        "supplier",
        "status",
        "created_date",
        "last_modified",
    ]


@admin.register(RFQContractAward)
class RFQContractAwardAdmin(admin.ModelAdmin):
    # list_display = [
    #     "contract",
    #     "supplier",
    #     "status",
    #     "created_date",
    #     "last_modified",
    # ]
    pass


@admin.register(RFQNegotiation)
class RFQNegotiationAdmin(admin.ModelAdmin):
    list_display = [
        "contract",
        "status",
        "created_date",
    ]


@admin.register(RFQNegotiationNote)
class RFQNegotiationNoteAdmin(admin.ModelAdmin):
    list_display = [
        "contract",
        "author",
        "pricing",
        "accepted",
        "renegotiated",
        "last_modified",
    ]
