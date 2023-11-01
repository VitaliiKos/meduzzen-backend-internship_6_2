from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import RequestModel
from apps.invitations.tests.base_test import BaseTestCase
from apps.users.models import UserModel as User
from core.enums.request_enum import RequestStatusEnum

UserModel: User = get_user_model()


class UserRequestActionsViewTestCase(BaseTestCase):
    """Test case for the UserRequestActionsView, which handles various user request actions."""

    def setUp(self):
        user = UserModel.objects.get(pk=2)
        self._authentication(user=user)

    def test_create_user_request(self):
        """Test the creation of a user request to join a company."""
        request_count = RequestModel.objects.count()
        employee_count = EmployeeModel.objects.count()
        query_params = {'company_id': 3}
        url = reverse('user_request_list')
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(RequestModel.objects.count(), request_count + 1)
        self.assertEqual(response.data['status'], RequestStatusEnum.PENDING.value)

    def test_get_user_request_list(self):
        """Test retrieving a list of user join requests."""
        user_requests = RequestModel.objects.filter(user=2, status=RequestStatusEnum.PENDING.value).count()

        response = self.client.get(reverse('user_request_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), user_requests)

    def test_cancel_request(self):
        """Test canceling a user's request."""
        user_request = RequestModel.objects.get(company=4, user=2)

        url = reverse('user_request_action', args=[user_request.id])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], RequestStatusEnum.CANCELED.value)
