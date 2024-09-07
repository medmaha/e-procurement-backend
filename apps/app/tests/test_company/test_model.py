from django.test import TestCase
from django.utils.text import slugify
from apps.app.models.company import Company

from .constants import COMPANY_NAME, COMPANY_EMAIL


class CompanyTestCase(TestCase):
    def setUp(self):
        self.company = Company(name=COMPANY_NAME, contact_email=COMPANY_EMAIL)

    def tearDown(self):
        self.company.delete()
        self.assertTrue(Company.objects.count() == 0)

    def test_save(self):
        # Test save verify slug
        self.company.save()
        self.assertIn(
            slugify(COMPANY_NAME),
            self.company.slug,
        )

    def test_required_fields(self):
        self.assertTrue(self.company)  # check if object is created
        self.assertEqual(self.company.name, COMPANY_NAME)  # check if name is correct
        self.assertEqual(str(self.company), COMPANY_NAME)  # check if __str__ is correct
        # check if contact email is correct
        self.assertEqual(COMPANY_EMAIL, self.company.contact_email)
