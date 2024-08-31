from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView

from apps.procurement.api.serializers.requisition import (
    Requisition,
    RequisitionRetrieveSerializer,
)

from .serializer import (
    RFQ,
    RFQResponse,
    Form101RFQSerializer,
    Form101RFQRequestSerializer,
    Form101RFQResponseSerializer,
)


class Form101RetrieveView(GenericAPIView):
    def get_query_params(self) -> dict[str, str]:
        return self.request.query_params or {}  # type: ignore

    def get_queryset(self):
        query_params = self.get_query_params()
        model_id = query_params.get("i")
        model_name = query_params.get("m")
        queryset = None

        try:
            model_id = int(model_id or 0)
            if model_id < 1:
                raise
        except:
            msg = "Invalid id lookup provided"
            return msg

        if model_name == "rfq":
            self.serializer_class = Form101RFQSerializer
            queryset = get_object_or_404(RFQ, pk=model_id)
        if model_name == "rfq-request":
            self.serializer_class = Form101RFQRequestSerializer
            queryset = get_object_or_404(RFQ, pk=model_id)
        elif model_name == "rfq_r":
            self.serializer_class = Form101RFQResponseSerializer
            queryset = get_object_or_404(RFQResponse, pk=model_id)
        elif model_name == "requisition":
            queryset = get_object_or_404(Requisition, pk=model_id)
            self.serializer_class = RequisitionRetrieveSerializer

        if not queryset:
            msg = "Invalid query params provided"
            return msg

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if isinstance(queryset, str):
            return Response({"message": queryset}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(
            instance=queryset, context={"request": request}
        )
        return Response({"data": serializer.data})
