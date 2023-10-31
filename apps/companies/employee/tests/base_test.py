from model_bakery import baker
from rest_framework.test import APITestCase

from apps.companies.employee.models import EmployeeModel
from apps.companies.models import CompanyModel
from apps.users.models import UserModel
from core.enums.user_enum import UserEnum


class BaseTestCase(APITestCase):
    """Base test case for common setup and utility functions."""

    def setUp(self):
        """Set up common data for test cases."""
        self.owner = baker.make(UserModel)
        self.company = baker.make(CompanyModel)
        self.member = baker.make(UserModel)
        baker.make(EmployeeModel, user=self.owner, company=self.company, role=UserEnum.OWNER.value)
        baker.make(EmployeeModel, user=self.member, company=self.company, role=UserEnum.MEMBER.value)

    def _authentication(self, user):
        """Set the authentication credentials using the provided token."""
        self.client.force_authenticate(user=user)
