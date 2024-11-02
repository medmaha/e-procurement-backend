from django.contrib import admin

from ..models import contract
from ..models import contract_award


@admin.register(contract.Contract)
class ContractAdmin(admin.ModelAdmin):
    pass


@admin.register(contract.ContractAttachment)
class ContractAttachmentAdmin(admin.ModelAdmin):
    pass


# Awards
@admin.register(contract_award.ContractAward)
class ContractAwardAdmin(admin.ModelAdmin):
    pass


@admin.register(contract_award.ContractAwardApproval)
class ContractAwardApprovalAdmin(admin.ModelAdmin):
    pass
