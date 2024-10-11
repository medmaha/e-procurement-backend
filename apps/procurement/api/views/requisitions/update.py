from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.procurement.api.serializers.requisition import (
    RequisitionUpdateSerializer,
    RequisitionItemSerializer,
)
from apps.accounts.models import Account
from apps.procurement.models.requisition import Requisition, RequisitionItem


class RequisitionUpdateView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        data = request.data.copy()
        obj_id = data.get("meta", {}).get("id")
        instance = Requisition.objects.filter(id=obj_id).first()
        if not instance:
            return Response(
                {"message": "Requisition identifier not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            items = data.pop("items")
            instance_items = instance.items.all()
        except:
            return Response(
                {"message": "Failed to create requisition", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RequisitionUpdateSerializer(instance=instance, data=data)
        items_serializer = RequisitionItemSerializer(data=items, many=True)

        if serializer.is_valid() and items_serializer.is_valid():
            items_to_delete = []
            items_to_create = []
            items_to_update = []
            items_to_update_pks = []
            for i in instance_items:
                item: RequisitionItem = i
                found = False
                for j in items:
                    item_id = j.get("id")
                    if str(item.pk) == item_id:
                        for key, value in j.items():
                            if key != "id":
                                setattr(item, key, value)
                                found = True
                                items_to_update.append(item)
                                items_to_update_pks.append(item.pk)

                    if not item_id:
                        try:
                            if j.get("description") in items_to_create:
                                continue
                            _data = {
                                "description": j.get("description"),
                                "quantity": int(j.get("quantity")),
                                "unit_cost": Decimal(j.get("unit_cost")),
                                "measurement_unit": j.get("measurement_unit"),
                                "remark": j.get("remark"),
                            }

                            _i, _ = RequisitionItem.objects.get_or_create(**_data)
                            instance.items.add(_i)
                            items_to_create.append(_data["description"])
                        except Exception as e:
                            return Response(
                                {
                                    "message": "Failed to create requisition -->%s --> %s"
                                    % (j.get("description"), e),
                                    "success": False,
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                if not found:
                    items_to_delete.append(item.pk)

            if items_to_delete:
                RequisitionItem.objects.filter(pk__in=items_to_delete).delete()
            if items_to_update:
                RequisitionItem.objects.filter(pk__in=items_to_update_pks).bulk_update(
                    items_to_update,
                    [
                        "quantity",
                        "unit_cost",
                        "measurement_unit",
                        "description",
                        "remark",
                    ],
                )

            serializer.save(officer=profile)
            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Failed to create requisition", "success": False},
            status=status.HTTP_400_BAD_REQUEST,
        )
