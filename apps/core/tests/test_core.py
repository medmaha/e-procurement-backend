from rest_framework.test import APITestCase, APIClient
from apps.accounts.models import Account


class TextCore(APITestCase):

    fixtures = ["index"]

    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.first()

    def test_200_ok(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_leading_slash(self):

        without_leading_slash_response = self.client.get("/test")
        self.assertEqual(without_leading_slash_response.status_code, 301)

        without_leading_slash_response = self.client.get("/test/")
        self.assertEqual(without_leading_slash_response.status_code, 200)

    def test_api_404_not_found(self):
        response = self.client.get("/api/not-found/")
        self.assertEqual(response.status_code, 404)

        data: dict = response.data  # type: ignore

        self.assertIn("error", data)
        self.assertIn("message", data)
        self.assertEqual(response.status_code, data["status"])

        self.assertIn("request", data)
        self.assertIn("Origin", data["request"])
        self.assertIn("Hash-Key", data["request"])
        self.assertIn("Client Agent", data["request"])
        self.assertNotIn("Authentication", data["request"])
        self.assertEqual("API SERVER", data["request"]["Intent"])

    def test_404_not_found(self):
        response = self.client.get("/not-found/")
        self.assertEqual(response.status_code, 404)

        data: dict = response.data  # type: ignore

        self.assertIn("error", data)
        self.assertIn("message", data)
        self.assertEqual(response.status_code, data["status"])

        self.assertIn("request", data)
        self.assertIn("Origin", data["request"])
        self.assertIn("Hash-Key", data["request"])
        self.assertIn("Client Agent", data["request"])
        self.assertNotIn("Authentication", data["request"])
        self.assertEqual("WEB SERVER", data["request"]["Intent"])

    def test_404_not_found_authenticated(self):
        self.client.force_authenticate(user=self.user)  # type: ignore
        response = self.client.get("/not-found/")
        self.assertEqual(response.status_code, 404)

        data: dict = response.data  # type: ignore
        self.assertIn("User", data["request"])
        self.assertIn("Full Name", data["request"]["User"])
        self.assertIn("Account Type", data["request"]["User"])
        self.assertEqual(data["request"]["Authenticated"], True)
