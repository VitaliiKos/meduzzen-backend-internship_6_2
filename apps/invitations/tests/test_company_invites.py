from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import InviteModel
from apps.invitations.tests.base_test import BaseTestCase
from apps.users.models import UserModel as User
from core.enums.invite_enum import InviteStatusEnum

UserModel: User = get_user_model()


class CompanyInviteActionsView(BaseTestCase):
    """Test case for the CompanyInviteActionsView, which handles various company invite and request actions."""

    def setUp(self):
        user = UserModel.objects.get(pk=1)
        self._authentication(user=user)

    def test_create_company_invite(self):
        """Test the creation of a company invite."""
        invite_count = InviteModel.objects.count()
        employee_count = EmployeeModel.objects.count()
        query_params = {'user_id': 4, "company_id": 1}
        url = reverse('invitation_list')
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))

        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(InviteModel.objects.count(), invite_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], InviteStatusEnum.PENDING.value)

    #
    def test_get_company_invites_list(self):
        """Test retrieving a list of company invites."""
        company_invites = InviteModel.objects.filter(company=1, status=InviteStatusEnum.PENDING.value).count()
        query_params = {"company_id": 1}
        url = reverse('invitation_list')
        response = self.client.get(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), company_invites)

    def test_revoke_invite(self):
        """Test revoking a company invite."""
        invite = InviteModel.objects.get(company=1, user=3)
        query_params = {"company_id": 1}
        url = reverse('invitation_action', args=[invite.id])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], InviteStatusEnum.REVOKED.value)
