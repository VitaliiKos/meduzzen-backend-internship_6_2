from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.invitations.models import RequestModel
from apps.invitations.tests.base_test import BaseTestCase
from apps.users.models import UserModel as User
from core.enums.invite_enum import InviteStatusEnum
from core.enums.request_enum import RequestStatusEnum

UserModel: User = get_user_model()


class CompanyRequestActionsViewTestCase(BaseTestCase):
    """Test case for the CompanyInviteActionsView, which handles various company request actions."""

    def setUp(self):
        user = UserModel.objects.get(pk=1)
        self._authentication(user=user)

    def test_get_company_request_list(self):
        """Test retrieving a list of company join requests."""
        company_requests = RequestModel.objects.filter(company=1, status=InviteStatusEnum.PENDING.value).count()
        query_params = {'company_id': 1}
        url = reverse('request_list')
        response = self.client.get(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), company_requests)

    def test_approve_request(self):
        """Test approving a company join request."""
        user_request = RequestModel.objects.get(company=1, user=5, status=InviteStatusEnum.PENDING.value)
        query_params = {'company_id': 1, 'status': RequestStatusEnum.APPROVED.value}
        url = reverse('request_action', args=[user_request.id])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], RequestStatusEnum.APPROVED.value)

    def test_reject_request(self):
        """Test rejecting a company join request."""
        user_request = RequestModel.objects.get(company=1, user=5, status=InviteStatusEnum.PENDING.value)
        query_params = {'company_id': 1, 'status': RequestStatusEnum.REJECTED.value}
        url = reverse('request_action', args=[user_request.id])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], RequestStatusEnum.REJECTED.value)
