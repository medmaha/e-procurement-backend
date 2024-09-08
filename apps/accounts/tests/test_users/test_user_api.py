from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import Account
from ..constants import USERS_API_URL


class TestAccountAPI(TestCase):

    fixtures = ["index"]

    def setUp(self):
        self.account = Account.objects.get(is_superuser=True)

        self.client = APIClient()
        self.client.force_authenticate(user=self.account)

    def test_accounts_list(self):
        """Get list of users"""

        response = self.client.get(f"{USERS_API_URL}/", format="json")

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 200)

        # make sure response is paginated
        self.assertTrue(response_dict["count"] > 0)
        self.assertTrue(isinstance(response_dict["results"], list))

        if len(response_dict["results"]) > 0:
            self.assertIn("full_name", response_dict["results"][0])

        return response

    def test_accounts_query(self):
        """Get list of users"""

        response = self.client.get(
            f"{USERS_API_URL}/query/?q={self.account.email}", format="json"
        )

        self.assertEqual(response.status_code, 200)
        response_dict: dict = response.data  # type: ignore

        # make sure response is paginated
        self.assertTrue(response_dict["count"] == 1)
        self.assertTrue(isinstance(response_dict["results"], list))

        self.assertEqual(
            response_dict["results"][0]["full_name"], self.account.full_name
        )

        return response

    def test_accounts_get(self):
        """Get single user"""

        response = self.client.get(
            f"{USERS_API_URL}/{str(self.account.id)}/", format="json"
        )

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 200)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the user_id
        self.assertEqual(response_dict.get("id"), str(self.account.id))

    def test_accounts_create(self):
        """Create user and get single user"""

        data = {
            "password": "test",
            "first_name": "Test",
            "last_name": "User",
            "email": "3Jq6G@example.com",
        }

        response = self.client.post(f"{USERS_API_URL}/create/", data, format="json")

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 201)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the user's name
        self.assertIn(data["first_name"], response_dict["full_name"])

    def test_accounts_update(self):
        """Create user and get single user"""

        data = {
            "first_name": "Test Updated",
            "last_name": "User Updated",
        }

        response = self.client.put(
            f"{USERS_API_URL}/{str(self.account.id)}/update/", data, format="json"
        )

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 200)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the user's name
        self.assertIn(data["first_name"], response_dict["full_name"])

        account = Account.objects.get(is_superuser=True)
        self.assertEqual(data["first_name"], account.first_name)

    def test_accounts_delete(self):
        """Create user and get single user"""

        response = self.client.delete(
            f"{USERS_API_URL}/{str(self.account.id)}/disable/", format="json"
        )

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 204)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the message
        self.assertIn("message", response_dict)
