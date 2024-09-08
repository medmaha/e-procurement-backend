from rest_framework.test import APIClient
from django.test import TestCase

from apps.accounts.models import Account
from apps.vendors.models import Vendor
from apps.organization.models import Staff
from ..constants import AUTH_API_URL


class TestLoginAPI(TestCase):

    fixtures = ["index"]

    def setUp(self):
        self.client = APIClient()

    def validate_response(self, response, status_code=200):
        response_dict: dict = response.data  # type: ignore

        self.assertTrue(isinstance(response_dict, dict))

        self.assertEqual(response.status_code, status_code)

        if response.status_code == 200:
            self.assertIn("access", response_dict)
            self.assertIn("refresh", response_dict)
            self.assertTrue(isinstance(response_dict.get("access"), str))

            # the token should not be empty
            self.assertTrue(len(response_dict["access"]) > 0)

        else:
            self.assertIn("error", response_dict)

        return response

    def test_login_api(self):
        account = Account.objects.get(is_superuser=True)

        if not account:
            return self.assertIsNotNone(account)

        self.credentials = {
            "email": account.email,
            "password": "admin",
        }
        response = self.client.post(
            AUTH_API_URL + "/login/", data=self.credentials, format="json"
        )

        return self.validate_response(response, status_code=200)

    def test_staff_login_api(self):
        staff = Staff.objects.first()

        if not staff:
            return self.assertIsNotNone(staff)
        self.credentials = {
            "email": staff.user_account.email,
            "password": staff.user_account.DEFAULT_PASSWORD,
        }
        response = self.client.post(
            AUTH_API_URL + "/login/", data=self.credentials, format="json"
        )

        return self.validate_response(response, status_code=200)

    def test_vendor_login_api(self):
        vendor = Vendor.objects.first()

        if not vendor:
            return self.assertIsNotNone(vendor)
        self.credentials = {
            "email": vendor.user_account.email,
            "password": vendor.user_account.DEFAULT_PASSWORD,
        }
        response = self.client.post(
            AUTH_API_URL + "/login/", data=self.credentials, format="json"
        )

        return self.validate_response(response, status_code=200)

    def test_login__api_with_bad_credentials(self):
        response = self.client.post(
            AUTH_API_URL + "/login/",
            data={
                "email": "badass@email.com",
                "password": "bad-ass-password",
            },
            format="json",
        )

        return self.validate_response(response, status_code=401)
