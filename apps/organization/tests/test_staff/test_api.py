from rest_framework.test import APITestCase, APIClient

from apps.accounts.models import Account
from apps.organization.models import Staff, Unit

from ..constants import ORGANIZATION_API_URL


class TestStaffApi(APITestCase):

    fixtures = ["index"]

    def setUp(self):

        self.user = Account.objects.get(staff_account__isnull=False)
        self.staff = self.user.staff_account.first()  # type: ignore

        self.client = APIClient()

        self.client.force_authenticate(user=self.user)

    def test_staffs_api_list(self):
        """Test Staff API List View"""
        response = self.client.get(f"{ORGANIZATION_API_URL}/staffs/", format="json")

        # check if status code is 200
        self.assertEqual(response.status_code, 200)

        data: dict = response.data  # type: ignore

        # check if response is paginated
        self.assertTrue("count" in data)
        self.assertTrue("next" in data)
        self.assertTrue("previous" in data)
        self.assertTrue("results" in data)

        # check if results is array
        self.assertTrue(isinstance(data["results"], list))

        # check if response is serialized
        self.assertIn("id", data["results"][0])

    def test_staffs_api_query(self):
        """Test Staff API List View"""
        response = self.client.get(
            f"{ORGANIZATION_API_URL}/staffs/query/?q={self.user.first_name}",
            format="json",
        )

        # check if status code is 200
        self.assertEqual(response.status_code, 200)

        data: dict = response.data  # type: ignore

        # check if response is paginated
        self.assertTrue("count" in data)
        self.assertTrue("next" in data)
        self.assertTrue("previous" in data)
        self.assertTrue("results" in data)

        # check if results is array
        self.assertTrue(isinstance(data["results"], list))

        # check if response is serialized
        self.assertTrue("id" in data["results"][0])

        self.assertTrue(str(self.staff.pk) == data["results"][0]["id"])  # type: ignore

    def test_staff_api_retrieve(self):
        """Test staff api retrieve with slug"""

        response = self.client.get(
            f"{ORGANIZATION_API_URL}/staffs/{self.staff.pk}/",
        )

        staff_dict: dict = response.data  # type: ignore

        self.assertTrue(isinstance(staff_dict, dict))

        # check if status code is 200
        self.assertTrue(response.status_code, 200)
        self.assertIn("id", staff_dict)

        self.assertTrue(str(self.staff.pk) == staff_dict["id"])

    def test_staff_api_delete(self):
        """Test staff api delete"""

        response = self.client.delete(
            f"{ORGANIZATION_API_URL}/staffs/{self.staff.id}/disable/",
        )
        # check if status code is 204
        self.assertEqual(response.status_code, 204)

    def test_staff_api_update(self):
        """Test staff api update"""

        data = {
            "phone": "2478562",
            "gender": "Male",
        }
        response = self.client.put(
            f"{ORGANIZATION_API_URL}/staffs/{self.staff.id}/update/", data
        )

        staff_dict: dict = response.data  # type: ignore

        # check if response is not empty
        self.assertTrue(isinstance(staff_dict, dict))

        # check if status code is 200
        self.assertEqual(response.status_code, 200)
        # check if name is updated
        self.assertEqual(staff_dict.get("phone"), data["phone"])
        self.assertEqual(staff_dict.get("gender"), data["gender"])

        self.assertFalse(
            staff_dict["phone"] == self.staff.phone, "The phone was not updated"
        )
        self.assertFalse(
            staff_dict["gender"] == self.staff.gender, "The gender was not updated"
        )

    def test_staff_api_create(self):
        """Test staff api create"""

        unit = Unit.objects.first()

        if not unit:
            return self.assertNotEqual(unit, None, "There is no unit in the system")

        account = Account.objects.create(
            first_name="John",
            last_name="Doe",
            email="X9L0N@example.com",
            password="12345678",
        )

        data = {
            "phone": "2478562",
            "gender": "Male",
            "unit": unit.pk,
            "user_account": account.pk,
        }

        response = self.client.post(f"{ORGANIZATION_API_URL}/staffs/create/", data)

        staff_dict: dict = response.data  # type: ignore

        # check if response is not empty
        self.assertTrue(isinstance(staff_dict, dict))

        # check if status code is 200
        self.assertEqual(response.status_code, 201)

        # check if name is updated
        self.assertEqual(staff_dict.get("phone"), data["phone"])
        self.assertEqual(staff_dict.get("gender"), data["gender"])

        self.assertFalse(
            staff_dict["phone"] == self.staff.phone, "The phone was not updated"
        )
        self.assertFalse(
            staff_dict["gender"] == self.staff.gender, "The gender was not updated"
        )

        # count number staffs
        staffs = Staff.objects.all()
        self.assertEqual(staffs.count(), 2)
