from ...models.company import Company
from rest_framework import serializers


class CompanyCreateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False)

    class Meta:
        model = Company
        fields = "__all__"


class CompanyUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    contact_email = serializers.EmailField(required=False)
    contact_phone = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    coordinates = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    industry = serializers.CharField(required=False)
    website_url = serializers.URLField(required=False)
    tax_id = serializers.CharField(required=False)
    postal_code = serializers.CharField(required=False)
    license_number = serializers.CharField(required=False)
    registration_number = serializers.CharField(required=False)
    registration_certificate_url = serializers.URLField(required=False)

    class Meta:
        model = Company
        fields = [
            "name",
            "contact_email",
            "contact_phone",
            "city",
            "address",
            "coordinates",
            "country",
            "industry",
            "website_url",
            "tax_id",
            "postal_code",
            "license_number",
            "registration_number",
            "registration_certificate_url",
        ]


class CompanyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "slug",
            "contact_email",
            "contact_phone",
            "city",
            "address",
            "coordinates",
            "country",
            "industry",
            "website_url",
            "tax_id",
            "postal_code",
            "license_number",
            "registration_number",
            "registration_certificate_url",
            "verified",
            "date_verified",
            "created_date",
            "last_modified",
        ]


class CompanyQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "slug",
            "address",
            "country",
            "industry",
            "website_url",
            "verified",
            "date_verified",
            "created_date",
        ]
