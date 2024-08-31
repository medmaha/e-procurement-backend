from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from apps.vendors.models import Invoice
from apps.vendors.api.serializers.invoices import InvoiceListSerializer


class InvoiceListView(ListAPIView):
    serializer_class = InvoiceListSerializer

    def get_queryset(self, profile_type, profile):
        if profile_type == "Vendor":
            return Invoice.objects.filter(vendor=profile)
        return Invoice.objects.filter()

    def list(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()  # type: ignore
        queryset = self.get_queryset(profile_type, profile)
        serializer = self.get_serializer(
            self.filter_queryset(queryset), many=True, context={"request": request}
        )
        return Response({"data": serializer.data})
