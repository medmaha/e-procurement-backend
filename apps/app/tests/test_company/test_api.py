from django.test import TestCase
from rest_framework.test import APIClient
from apps.app.models.company import Company
from apps.accounts.models import Account

from .constants import COMPANY_API_URL, COMPANY_NAME, COMPANY_EMAIL


class CompanySuccessAPITestCase(TestCase):

    def setUp(self):

        self.company = Company.objects.create(
            name=COMPANY_NAME, contact_email=COMPANY_EMAIL
        )

        self.user = Account.objects.create(
            first_name="Test",
            last_name="User",
            is_superuser=True,
            is_staff=True,
            email="test@me.com",
            password="prc@2k2*",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.api_company_dict: dict | None = None

    def test_company_api_create(self):
        """Test company api create"""
        data = {
            "name": COMPANY_NAME,
            "contact_email": "test2@me.com",
        }
        response = self.client.post(
            f"{COMPANY_API_URL}/create/",
            data,
        )
        # check if status code is 201
        self.assertTrue(response.status_code, 201)

        company_dict = response.data
        self.api_company_dict = response.data

        # check if response is not empty
        self.assertTrue(isinstance(company_dict, dict))

        # Make sure the slugs are different
        # Even though the names are the same
        self.assertTrue(self.company.slug != company_dict.get("slug"))
        # Make sure the slugs are longer
        self.assertTrue(len(self.company.slug) < len(company_dict.get("slug")))

    def test_company_api_retrieve(self):
        """Test company api retrieve with slug"""

        slug = self.company.slug
        response = self.client.get(
            f"{COMPANY_API_URL}/{slug}/",
        )
        # check if status code is 200
        self.assertTrue(response.status_code, 200)
        # check if response is not empty
        self.assertTrue(isinstance(response.data, dict))

    def test_company_api_update(self):
        """Test company api update"""

        name = "Test Company 2"
        response = self.client.put(
            f"{COMPANY_API_URL}/{self.company.slug}/update/",
            {
                "name": name,
            },
        )

        company_dict = response.data

        # check if status code is 200
        self.assertTrue(response.status_code, 200)
        # check if response is not empty
        self.assertTrue(isinstance(company_dict, dict))
        # check if name is updated
        self.assertTrue(company_dict.get("name") == name)

    def test_company_api_list(self):
        """Test company api list"""
        response = self.client.get(
            f"{COMPANY_API_URL}/",
        )
        # check if status code is 200
        self.assertEqual(response.status_code, 200)

        company_dict = response.data

        # check if response is not empty
        # because we're paginating the response
        self.assertTrue(isinstance(company_dict, dict))
        self.assertTrue(isinstance(company_dict.get("results"), list))

        # check if company count is greater than 0
        self.assertTrue(len(company_dict.get("results")) > 0)

    def test_company_api_delete(self):
        """Test company api delete"""

        response = self.client.delete(
            f"{COMPANY_API_URL}/{self.company.slug}/delete/",
        )
        # check if status code is 204
        self.assertEqual(response.status_code, 204)

    def test_company_api_query(self):
        """Test company api query"""
        response = self.client.get(
            f"{COMPANY_API_URL}/query/?q=Test",
        )

        # check if status code is 200
        self.assertEqual(response.status_code, 200)

        company_dict = response.data

        # check if response is not empty
        # because we're paginating the response
        self.assertTrue(isinstance(company_dict, dict))
        self.assertTrue(isinstance(company_dict.get("results"), list))

        # check if company count is greater than 0
        self.assertTrue(len(company_dict.get("results")) > 0)

    def tearDown(self):
        Company.objects.filter(name__icontains="Test").delete()
        self.assertTrue(Company.objects.count() == 0)


class CompanyFailureAPITestCase(TestCase):

    def setUp(self):
        self.user = Account.objects.create(
            first_name="Test",
            last_name="User",
            is_superuser=True,
            is_staff=True,
            email="test@me.com",
            password="prc@2k2*",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_company_api_create(self):
        """Test company api create"""
        data = {
            "name": COMPANY_NAME,
        }

        response = self.client.post(
            f"{COMPANY_API_URL}/create/",
            data,
        )
        # check if status code is 400
        self.assertTrue(response.status_code, 400)

        error = response.data
        self.assertTrue("contact_email" in error.get("error", "").lower())

    def test_company_api_retrieve(self):
        """Test company api retrieve with slug"""

        slug = "test-company"
        response = self.client.get(
            f"{COMPANY_API_URL}/{slug}/",
        )
        # check if status code is 404
        self.assertTrue(response.status_code, 404)
        self.assertTrue("not found" in response.data.get("error", ""))

    def test_company_api_update(self):
        """Test company api update"""

        name = "Test Company 2"
        response = self.client.put(
            f"{COMPANY_API_URL}/test-company/update/",
            {
                "name": name,
            },
        )

        company_dict = response.data

        # check if status code is 404
        self.assertTrue(response.status_code, 404)
        self.assertTrue("not found" in company_dict.get("error", ""))

    def test_company_api_list(self):
        """Test company api list"""

        self.client.logout()

        response = self.client.get(
            f"{COMPANY_API_URL}/",
        )

        # check if status code is 401
        self.assertTrue(response.status_code, 401)

        self.assertTrue("detail" in response.data)

    def tearDown(self):
        self.user.delete()
