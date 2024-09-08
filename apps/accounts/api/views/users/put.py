from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.accounts.models import Account
from apps.core.utilities.errors import get_serializer_error_message

from ...serializers.users import AccountUpdateSerializer, AccountRetrieveSerializer


class AccountUpdateView(UpdateAPIView):
    serializer_class = AccountUpdateSerializer

    def update(self, request, user_id, *args, **kwargs):

        try:
            account = get_object_or_404(Account, pk=user_id)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=404)

        serializer = self.get_serializer(instance=account, data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            result_serializer = AccountRetrieveSerializer(instance=user)
            return Response(result_serializer.data, status=200)

        error_message = get_serializer_error_message(serializer)
        return Response({"error": error_message}, status=400)
