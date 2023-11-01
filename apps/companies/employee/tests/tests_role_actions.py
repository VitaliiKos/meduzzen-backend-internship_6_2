from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from apps.companies.employee.models import EmployeeModel
from apps.companies.employee.tests.base_test import BaseTestCase
from core.enums.user_enum import UserEnum

UserModel = get_user_model()


class MemberRoleActionViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.member2 = baker.make(UserModel)
        baker.make(EmployeeModel, user=self.member2, company=self.company, role=UserEnum.ADMIN.value)

        self._authentication(self.owner)

    def test_list_admins(self):
        """Test listing admins of a company."""
        query_params = {"company_id": self.company.id}
        url = reverse('admin_role_action')

        response = self.client.get(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_user_to_admin(self):
        """Test promoting a member to an admin role."""
        count_admin_before = EmployeeModel.objects.filter(company=self.company.id, role=UserEnum.ADMIN.value).count()
        query_params = {"company_id": self.company.id, "user_id": self.member.id, "role": UserEnum.ADMIN.value}

        url = reverse('admin_role_action')
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))

        count_admin_after = EmployeeModel.objects.filter(company=self.company.id, role=UserEnum.ADMIN.value).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], UserEnum.ADMIN.value)
        self.assertEqual(count_admin_after, count_admin_before + 1)

    def test_admin_to_user(self):
        """Test demoting an admin to a member role."""
        count_admin_before = EmployeeModel.objects.filter(company=self.company.id, role=UserEnum.ADMIN.value).count()
        query_params = {"company_id": self.company.id, "user_id": self.member2.id, "role": UserEnum.MEMBER.value}

        url = reverse('admin_role_action')
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))

        count_admin_after = EmployeeModel.objects.filter(company=self.company.id, role=UserEnum.ADMIN.value).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], UserEnum.MEMBER.value)
        self.assertEqual(count_admin_after, count_admin_before - 1)
