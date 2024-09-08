from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.core.utilities.errors import get_serializer_error_message

from ...serializers.users import AccountCreateSerializer, AccountRetrieveSerializer


class AccountCreateView(CreateAPIView):
    serializer_class = AccountCreateSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            result_serializer = AccountRetrieveSerializer(instance=user)
            return Response(result_serializer.data, status=201)

        error_message = get_serializer_error_message(serializer)
        return Response({"error": error_message}, status=400)
