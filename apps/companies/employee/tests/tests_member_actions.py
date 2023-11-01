from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.companies.employee.tests.base_test import BaseTestCase

User = get_user_model()


class EmployeeActionViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self._authentication(self.owner)

    def test_list_employees(self):
        """Test listing employees of a company."""
        query_params = {"company_id": self.company.id}

        url = reverse('employee_action')
        response = self.client.get(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_remove_member(self):
        """Test removing a member from a company."""
        query_params = {"company_id": self.company.id, "user_id": self.member.id}
        url = reverse('employee_action')
        response = self.client.put(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data['role'])

    def test_owner_cannot_leave_company(self):
        """Test that the owner cannot leave the company."""
        query_params = {"company_id": self.company.id}
        url = reverse('employee_action')
        response = self.client.put(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_owner_can_remove_member(self):
        """Test that only the owner can remove a member from the company."""
        self._authentication(self.member)

        url = reverse('employee_action')
        query_params = {"company_id": self.company.id, "user_id": self.owner.id}
        response = self.client.put(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
