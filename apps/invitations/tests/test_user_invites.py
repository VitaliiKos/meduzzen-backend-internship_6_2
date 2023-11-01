from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.invitations.models import InviteModel
from apps.invitations.tests.base_test import BaseTestCase
from apps.users.models import UserModel as User
from core.enums.invite_enum import InviteStatusEnum

UserModel: User = get_user_model()


class UserInviteActionsViewTestCase(BaseTestCase):
    """Test case for the UserRequestActionsView, which handles various user invitation actions."""

    def setUp(self):
        user = UserModel.objects.get(pk=2)
        self._authentication(user=user)

    def test_get_user_invite_list(self):
        """Test retrieving a list of user invitations."""
        user_invites = InviteModel.objects.filter(user=2, status=InviteStatusEnum.PENDING.value).count()
        url = reverse('user_invites_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), user_invites)

    def test_accept_invite(self):
        """Test accepting a user invitation."""
        query_params = {"status": InviteStatusEnum.ACCEPTED.value}
        url = reverse('user_invites_action', args=['1'])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], InviteStatusEnum.ACCEPTED.value)

    def test_decline_invite(self):
        """Test declining a user invitation."""
        query_params = {"status": InviteStatusEnum.DECLINED.value}
        url = reverse('user_invites_action', args=['1'])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], InviteStatusEnum.DECLINED.value)
