from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.companies.employee.models import EmployeeModel
from apps.companies.models import CompanyModel
from core.enums.user_enum import UserEnum

User = get_user_model()


class EmployeeActionViewTest(APITestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user(email='owner_user@example.com', password='P@$$word1')
        self.member_user = User.objects.create_user(email='member_user@example.com', password='P@$$word1')
        self.company = CompanyModel.objects.create(name='Test Company')
        self.company.members.add(self.owner_user, through_defaults={'role': UserEnum.OWNER})
        self.employee = EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.MEMBER)

    def test_list_employees(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('employee_action', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.member_user.email, str(response.data))

    def test_remove_member(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('employee_action', args=[self.company.id])
        data = {'user_id': self.member_user.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EmployeeModel.objects.filter(user=self.member_user, company=self.company).count(), 1)

    def test_owner_cannot_leave_company(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('employee_action', args=[self.company.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_only_owner_can_remove_member(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('employee_action', args=[self.company.id])
        data = {'user_id': self.owner_user.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
