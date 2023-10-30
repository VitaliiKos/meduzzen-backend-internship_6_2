from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import InviteModel, RequestModel
from apps.users.models import UserModel as User
from core.enums.invite_enum import InviteStatusEnum
from core.enums.request_enum import RequestStatusEnum

UserModel: User = get_user_model()


class CompanyInviteActionsView(APITestCase):
    """Test case for the CompanyInviteActionsView, which handles various company invite and request actions."""
    fixtures = ["company_model_fixture", "employee_model_fixture", "invite_model_fixture", "request_model_fixture",
                "users_model_fixture"]

    def setUp(self):
        user = UserModel.objects.get(pk=1)
        self.client.force_authenticate(user=user)

    def _authentication(self, token):
        """Set the authentication credentials using the provided token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

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


class CompanyRequestActionsViewTestCase(APITestCase):
    """Test case for the CompanyInviteActionsView, which handles various company request actions."""
    fixtures = ["company_model_fixture", "employee_model_fixture", "invite_model_fixture", "request_model_fixture",
                "users_model_fixture"]

    def setUp(self):
        user = UserModel.objects.get(pk=1)
        self.client.force_authenticate(user=user)

    def _authentication(self, token):
        """Set the authentication credentials using the provided token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

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


class UserRequestActionsViewTestCase(APITestCase):
    """Test case for the UserRequestActionsView, which handles various user request and invitation actions."""
    fixtures = ["company_model_fixture", "employee_model_fixture", "invite_model_fixture", "request_model_fixture",
                "users_model_fixture"]

    def setUp(self):
        user = UserModel.objects.get(pk=2)
        self.client.force_authenticate(user=user)

    def _authentication(self, token):
        """Set the authentication credentials using the provided token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

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


class UserInviteActionsViewTestCase(APITestCase):
    """Test case for the UserRequestActionsView, which handles various user request and invitation actions."""
    fixtures = ["company_model_fixture", "employee_model_fixture", "invite_model_fixture", "request_model_fixture",
                "users_model_fixture"]

    def setUp(self):
        user = UserModel.objects.get(pk=2)
        self.client.force_authenticate(user=user)

    def _authentication(self, token):
        """Set the authentication credentials using the provided token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

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
