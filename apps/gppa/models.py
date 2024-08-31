from django.db import models

from apps.accounts.models.account import Account
from apps.core.utilities.generators import generate_unique_id


class GPPAUser(models.Model):
    user_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="gppa_account"
    )

    def __str__(self):
        return self.user_account.email

    def __getter__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        if hasattr(self.user_account, key):
            return getattr(self.user_account, key)
        return None
