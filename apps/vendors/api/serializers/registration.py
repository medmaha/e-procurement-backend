from rest_framework import serializers
from apps.vendors.models import VendorRegistration, Certificate


class VendorRegistrationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRegistration
        fields = [
            "id",
            "status",
            "is_validated",
            "created_date",
            "last_modified",
        ]

    def to_representation(self, instance: VendorRegistration):
        data = super().to_representation(instance)
        data["vendor"] = {
            "id": instance.vendor.pk,
            # "unique_id":instance.vendor.pk,
            "name": instance.vendor.name,
        }
        contact_person = instance.vendor.contact_person
        if contact_person:
            data["is_email_verified"] = contact_person.verified
        return data


class VendorRegistrationCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "name", "file"]


class VendorRegistrationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRegistration
        fields = "__all__"

    def to_representation(self, instance: VendorRegistration):
        data = super().to_representation(instance)
        data["vendor"] = {
            "id": instance.vendor.pk,
            "active": instance.vendor.active,
            "name": instance.vendor.name,
        }
        data["certificates"] = VendorRegistrationCertificateSerializer(
            instance=instance.vendor.certificates.filter(),
            many=True,
            context=self.context,
        ).data
        if instance.vendor.contact_person:
            data["contact_person"] = {
                "id": instance.vendor.contact_person.pk,
                "verified": instance.vendor.contact_person.verified,
                "name": instance.vendor.contact_person.full_name,
            }
            data["is_email_verified"] = instance.vendor.contact_person.verified

        return data
