from django.test import TestCase

from apps.accounts.models import Account
from apps.vendors.models import Vendor
from apps.organization.models import Staff


class TestAccountModel(TestCase):
    fixtures = ["index"]

    def setUp(self):
        self.user = Account(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.user.save()

    def test_account_is_active_false_by_default(self):
        is_active = self.user.is_active
        self.assertFalse(is_active)

    def test_account_save(self):
        self.assertIsNotNone(self.user.id)
        self.assertEqual(self.user.email, str(self.user))
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")

    def test_account_full_name(self):
        self.assertEqual(self.user.full_name, "Test User")

        user = Account(
            email="test2@example.com",
            password="testpassword",
            first_name="Test-1",
            last_name="User-2",
            middle_name="Middle",
        )
        user.save()

        self.assertEqual(user.full_name, "Test-1 Middle User-2")

    def test_account_get_profile(self):
        self.assertEqual(self.user.profile_type, "None")
        self.assertEqual(self.user.get_profile(), ("None", None))

        self.assertEqual(self.user.profile, None)
        self.assertTrue(isinstance(self.user.get_profile(), tuple))

        staff = Staff.objects.first()  # First Staff
        if not staff:
            return self.assertIsNotNone(staff)
        self.assertEqual(staff.user_account.get_profile(), ("Staff", staff))

        vendor = Vendor.objects.first()  # First Vendor
        if not vendor:
            return self.assertIsNotNone(vendor)
        self.assertEqual(vendor.user_account.get_profile(), ("Vendor", vendor))
