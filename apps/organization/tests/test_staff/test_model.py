from django.test import TestCase
from django.utils.text import slugify

from ...models import Staff, Unit, Department, Company

from apps.accounts.models import Account


class TestStaffModel(TestCase):

    def setUp(self):
        user = Account.objects.create(
            email="test@me.com",
            first_name="Test",
            last_name="User",
            password="prc@2k2*",
        )

        company = Company.objects.create(
            name="Test Company",
        )

        department = Department.objects.create(
            name="Test Department",
            company=company,
        )
        unit = Unit.objects.create(
            name="Test Unit",
            department=department,
        )

        self.user = user

        self.staff = Staff.objects.create(
            phone="123456789", unit=unit, user_account=user
        )

    def test_staff_saved(self):
        self.assertEqual(Staff.objects.count(), 1)
        self.assertIsNotNone(self.staff.unit)
        self.assertIsNotNone(self.staff.unit.department)
        self.assertIsNotNone(self.staff.unit.department.company)

        self.assertEqual(str(self.staff), str(self.user))
        self.assertEqual(self.staff.phone, "123456789")

    def test_staff_org_slugs(self):
        unit_slug = self.staff.unit.slug
        department_slug = self.staff.unit.department.slug
        company_slug = self.staff.unit.department.company.slug

        self.assertIn(department_slug, unit_slug)
        self.assertIn(company_slug, unit_slug)
        self.assertIn(company_slug, department_slug)

        self.assertEqual(slugify(self.staff.unit.department.company.name), company_slug)

    def test_staff_deleted(self):
        self.assertEqual(self.staff.unit.staffs.count(), 1)
        self.staff.delete()
        self.assertEqual(Staff.objects.count(), 0)
        self.assertEqual(self.staff.unit.staffs.count(), 0)
