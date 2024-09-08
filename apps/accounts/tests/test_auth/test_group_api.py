from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import Account, AuthGroup
from ..constants import AUTH_API_URL


class TestAccountAPI(TestCase):

    fixtures = ["index"]

    def setUp(self):
        self.account = Account.objects.get(staff_account__isnull=False)
        auth_group = AuthGroup()

        auth_group.editable = True
        auth_group.name = "Test Group"
        auth_group.description = "Test Description"
        auth_group.authored_by = str(self.account.staff_account.first().pk)  # type: ignore
        auth_group.company_id = str(self.account.staff_account.first().department.company.pk)  # type: ignore

        auth_group.save()

        self.auth_group = auth_group

        self.client = APIClient()
        self.client.force_authenticate(user=self.account)

    def test_groups_list(self):
        """Get list of groups"""

        response = self.client.get(f"{AUTH_API_URL}/groups/", format="json")

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 200)

        # make sure response is paginated
        self.assertTrue(response_dict["count"] > 0)
        self.assertTrue(isinstance(response_dict["results"], list))

        if len(response_dict["results"]) > 0:
            self.assertIn("name", response_dict["results"][0])

        return response

    def test_groups_query(self):
        """Search list of groups"""

        response = self.client.get(
            f"{AUTH_API_URL}/groups/query/?q={self.auth_group.name}", format="json"
        )

        self.assertEqual(response.status_code, 200)
        response_dict: dict = response.data  # type: ignore

        # make sure response is paginated
        self.assertTrue(response_dict["count"] == 1)
        self.assertTrue(isinstance(response_dict["results"], list))

        self.assertEqual(response_dict["results"][0]["name"], self.auth_group.name)

        return response

    def test_groups_get(self):
        """Get single group"""

        response = self.client.get(
            f"{AUTH_API_URL}/groups/{str(self.auth_group.pk)}/", format="json"
        )

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 200)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the user_id
        self.assertEqual(response_dict.get("id"), self.auth_group.pk)

    def test_groups_create(self):
        """Create group and get single group"""

        data = {
            "name": "Test Group New",
            "description": "Test Description",
            "permissions": [1],
        }

        response = self.client.post(
            f"{AUTH_API_URL}/groups/create/", data, format="json"
        )

        response_dict: dict = response.data  # type: ignore

        self.assertEqual(response.status_code, 201)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the user's name
        self.assertEqual(data["name"], response_dict["name"])
        self.assertEqual(data["description"], response_dict["description"])

    def test_groups_update(self):
        """Update group and get back the group"""

        data = {
            "name": "Test Group Updated",
            "description": "Test Description Updated",
        }

        response = self.client.put(
            f"{AUTH_API_URL}/groups/{str(self.auth_group.pk)}/update/",
            data,
            format="json",
        )

        response_dict: dict = response.data  # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the user's name
        self.assertIn(data["name"], response_dict["name"])

        group = AuthGroup.objects.get(pk=self.auth_group.pk)
        self.assertEqual(data["name"], group.name)

    def test_groups_delete(self):
        """Deleted auth groups"""

        response = self.client.delete(
            f"{AUTH_API_URL}/groups/{str(self.auth_group.pk)}/disable/", format="json"
        )

        response_dict: dict = response.data  # type: ignore
        self.assertEqual(response.status_code, 204)

        self.assertTrue(isinstance(response_dict, dict))

        # make sure response includes the message
        self.assertIn("message", response_dict)
