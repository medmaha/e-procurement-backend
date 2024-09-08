from django.utils import timezone
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView

from apps.accounts.models import Account


class AccountDeleteSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
        ]


class AccountDisableAPIView(DestroyAPIView):
    serializer_class = AccountDeleteSerializer

    def get_queryset(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except:
            return None

    def destroy(self, request, user_id, *args, **kwargs):
        # TODO: ensure necessary permissions

        queryset = self.get_queryset(user_id)

        if not queryset:
            return Response({"error": "Account not found"}, status=404)

        queryset.is_deleted = True
        queryset.date_deleted = timezone.now()
        queryset.save()

        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
