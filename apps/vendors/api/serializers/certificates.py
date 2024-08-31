from rest_framework import serializers
from apps.vendors.models import Certificate


class CertificateListSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        exclude = []

    def get_vendor(self, instance: Certificate):
        return {
            "id": instance.vendor.pk,  # type: ignore
            # "unique_id":instance.vendor.pk,
            "name": instance.vendor.name,  # type: ignore
        }


class CertificateRetrieveSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = "__all__"

    def get_vendor(self, instance: Certificate):
        return {
            "id": instance.vendor.pk,  # type: ignore
            # "unique_id":instance.vendor.pk,
            "name": instance.vendor.name,  # type: ignore
        }
