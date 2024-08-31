from rest_framework import serializers
from apps.vendors.models import ContactPerson
from apps.core.utilities.generators import generate_unique_id


class ContactPersonListSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = ContactPerson
        exclude = []

    def get_vendor(self, instance: ContactPerson):
        if instance.vendor:
            return {
                "id": instance.vendor.pk,  # type: ignore
                "name": instance.vendor.name,  # type: ignore
            }
        return {}

    def to_representation(self, instance: ContactPerson):
        data = super().to_representation(instance)
        data["unique_id"] = generate_unique_id(None, instance.pk)

        if instance.address:
            data["address"] = {"id": instance.pk, "string": instance.address.to_string}

        return data


class ContactPersonRetrieveSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = ContactPerson
        fields = "__all__"

    def get_vendor(self, instance: ContactPerson):
        if instance.vendor:
            return {
                "id": instance.vendor.pk,  # type: ignore
                "name": instance.vendor.name,  # type: ignore
            }
        return {}

    def to_representation(self, instance: ContactPerson):
        data = super().to_representation(instance)
        data["unique_id"] = generate_unique_id(None, instance.pk)
        if instance.address:
            data["address"] = {"id": instance.pk, "string": instance.address.to_string}

        return data
