import random
from rest_framework import serializers
from apps.vendors.models import Vendor, RFQResponse
from apps.organization.models.staff import Staff
from APP_COMPANY import APP_COMPANY
from apps.accounts.models.account import Account
from apps.organization.models.procurement_plan import AnnualPlan
from apps.procurement.models.rfq import RFQ, RFQItem
from apps.core.utilities.generators import generate_unique_id


class Form101ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "id",
            "item_description",
            "quantity",
            "measurement_unit",
            "eval_criteria",
        ]


class Form101VendorSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    unique_id = serializers.SerializerMethodField()
    contact_person = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            "id",
            "unique_id",
            "contact_person",
            "name",
            "location",
        ]

    def get_contact_person(self, obj: Vendor):
        return (obj.contact_person.full_name) if obj.contact_person else "N/A"

    def get_unique_id(self, obj):
        return generate_unique_id("S", obj.pk)

    def get_location(self, obj: Vendor):
        if obj.contact_person:
            return (
                obj.contact_person.address.to_string
                if obj.contact_person.address
                else None
            )


class Form101RFQRequestSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()
    items = Form101ItemsSerializer(many=True)

    class Meta:
        model = RFQ
        fields = [
            "id",
            "items",
            "created_date",
            "last_modified",
            "unique_id",
            "vendor",
        ]

    def get_vendor(self, instance: RFQ):
        request = self.context.get("request")
        if request:
            profile_type, profile = request.user.get_profile()
            if profile_type == "Vendor":
                vendor = instance.suppliers.filter(pk=profile.pk).first()
                if vendor:
                    serializer = Form101VendorSerializer(
                        vendor, context={"request": request}
                    )
                    return serializer.data
        return {
            "id": "N/A",
            "unique_id": "N/A",
            "contact_person": "N/A",
            "name": "N/A",
            "location": "N/A",
        }

    def to_representation(self, instance: RFQ):
        data = super().to_representation(instance)
        data["deadline"] = str(instance.required_date)
        data["title"] = str(instance.title)

        from_company = APP_COMPANY["name"]
        from_location = APP_COMPANY["address"]

        data["from"] = from_company

        data["fromLocation"] = from_location

        data["authorizedBy"] = str(instance.officer)
        data["gppaNumber"] = random.randrange(10000000000, 99999999999)

        # filter out all accounts that belongs to a auth group call OpenQuotation
        data["openedBY"] = get_open_by_staffs(instance)

        try:
            annual_plan = AnnualPlan.get_current_plan()
            if annual_plan:
                data["expense_office"] = annual_plan.title
        except Exception as e:
            print(str(e))

        return data


class Form101RFQSerializer(serializers.ModelSerializer):
    suppliers = serializers.SerializerMethodField()
    items = Form101ItemsSerializer(many=True)

    class Meta:
        model = RFQ
        fields = [
            "id",
            "items",
            "created_date",
            "last_modified",
            "unique_id",
            "suppliers",
        ]

    def get_suppliers(self, instance: RFQ):
        vendors = instance.suppliers.all()
        serializer = Form101VendorSerializer(vendors, many=True)
        return serializer.data

    def to_representation(self, instance: RFQ):
        data = super().to_representation(instance)
        data["deadline"] = str(instance.required_date)
        data["title"] = str(instance.title)
        data["vendor"] = {}

        from_company = APP_COMPANY["name"]
        from_location = APP_COMPANY["address"]

        data["from"] = from_company
        data["fromLocation"] = from_location

        data["authorizedBy"] = str(instance.officer)
        data["gppaNumber"] = random.randrange(10000000000, 99999999999)

        data["openedBy"] = get_open_by_staffs(instance)

        annual_plan = AnnualPlan.get_current_plan()
        if annual_plan:
            data["expense_office"] = annual_plan.title
        return data


class Form101RFQResponseSerializer(serializers.ModelSerializer):
    items = Form101ItemsSerializer(many=True)

    class Meta:
        model = RFQResponse
        fields = [
            "id",
            "items",
            "created_date",
            "last_modified",
            "unique_id",
        ]

    def to_representation(self, instance: RFQResponse):
        data = super().to_representation(instance)
        from_company = APP_COMPANY["name"]
        from_location = APP_COMPANY["address"]

        data["from"] = from_company
        data["fromLocation"] = from_location

        data["authorizedBy"] = str(instance.rfq.officer)
        data["gppaNumber"] = random.randrange(10000000000, 99999999999)

        # filter out all accounts that belongs to a auth group call OpenQuotation
        data["openedBY"] = get_open_by_staffs(instance.rfq)
        try:
            annual_plan = AnnualPlan.get_current_plan()
            if annual_plan:
                data["expense_office"] = annual_plan.title
            # data["expense_office"] = (
            #     AnnualPlan.get_current_plan().title  # type: ignore
            #     # instance.rfq.requisition.approval_record.procurement_approval.annual_procurement_plan.plan.department.name  # type: ignore
            # )
        except Exception as e:
            print(str(e))

        return data


class OpenedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "name"]

    def to_representation(self, instance: Staff):
        data = super().to_representation(instance)
        data["designation"] = instance.department.name  # type: ignore
        return data


def get_open_by_staffs(instance: RFQ):
    return OpenedBySerializer(instance.opened_by.filter(), many=True).data
