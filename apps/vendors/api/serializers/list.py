from rest_framework import serializers
from apps.vendors.models import Vendor


class VendorSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name"]
