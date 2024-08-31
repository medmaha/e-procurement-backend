from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)


from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings

from apps.accounts.models import Account
from apps.accounts.api.views.account.login import populate_token


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

        user_id = refresh.get("user_id", None)
        user: Account = Account.objects.filter(pk=user_id).first()  # type: ignore

        refresh = RefreshToken.for_user(user)
        token = populate_token(user, refresh)
        return {
            "refresh": str(refresh),
            "access": str(token.access_token),  # type: ignore
        }


class RefreshAuthSessionTokens(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
