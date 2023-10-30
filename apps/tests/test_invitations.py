from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import InviteModel, RequestModel
from core.enums.invite_enum import InviteStatusEnum
from core.enums.request_enum import RequestStatusEnum

fake = Faker()
UserModel = get_user_model()


class BaseTestCase(APITestCase):
    """Base test case for common setup and utility functions."""

    def setUp(self):
        """Set up common data for test cases."""
        self.owner_user_info = self.generate_user_info()
        self.member_user_info = self.generate_user_info()

        self.owner = self.client.post(reverse("usermodel-list"), self.owner_user_info)
        self.member = self.client.post(reverse("usermodel-list"), self.member_user_info)

        self.member_token = self.get_token(self.member_user_info)
        self.owner_token = self.get_token(self.owner_user_info)
        self.company = self.create_company()

        self._authentication(self.owner_token)

    def _authentication(self, token):
        """Set the authentication credentials using the provided token."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def get_token(self, user):
        """Get the access token for a user."""
        data = {
            "email": user["email"],
            "password": user['password'],
        }
        token = self.client.post(reverse("jwt-create"), data)
        return token.data['access']

    @staticmethod
    def generate_user_info():
        """Generate user data for a new user."""
        password = fake.password()
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "password": password,
            "re_password": password,
        }
        return data

    def create_company(self):
        """Create a company."""
        self._authentication(self.owner_token)

        data = {
            "name": fake.company(),
            "description": fake.text(max_nb_chars=50),
            "visible": True,
        }
        url = reverse('company_list')
        response = self.client.post(url, data)
        return response.data

    def create_company_invite(self, user_token):
        """Create a company invite for the user."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        query_params = {'user_id': self.member.data['id'], "company_id": self.company['id']}
        url = reverse('invitation_list')
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self._authentication(user_token)
        return response


class CompanyInviteActionsViewTestCase(BaseTestCase):
    """Test case for the CompanyInviteActionsView, which handles various company invite actions."""

    def setUp(self):
        super().setUp()
        self._authentication(self.owner_token)

    def test_create_company_invite(self):
        """Test the creation of a company invite."""
        invite_count = InviteModel.objects.count()
        employee_count = EmployeeModel.objects.count()
        query_params = {'user_id': self.member.data['id'], "company_id": self.company['id']}
        url = reverse('invitation_list')
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))

        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(InviteModel.objects.count(), invite_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], InviteStatusEnum.PENDING.value)

    def test_get_company_invites_list(self):
        """Test retrieving a list of company invites."""
        self.test_create_company_invite()

        query_params = {"company_id": self.company['id']}
        url = reverse('invitation_list')
        response = self.client.get(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_revoke_invite(self):
        """Test revoking a company invite."""
        self.test_create_company_invite()
        invite = InviteModel.objects.get(company=self.company['id'], user=self.member.data['id'])
        query_params = {"company_id": self.company['id']}
        url = reverse('invitation_action', args=[invite.id])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], InviteStatusEnum.REVOKED.value)


class CompanyRequestActionsViewTestCase(BaseTestCase):
    """Test case for the CompanyInviteActionsView, which handles various company request actions."""

    def setUp(self):
        super().setUp()
        self._authentication(self.owner_token)

    def create_user_request(self):
        """Create a user request to join a company."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        query_params = {'company_id': self.company['id']}
        url = reverse('user_request_list')
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self._authentication(self.owner_token)
        return response

    def test_get_company_request_list(self):
        """Test retrieving a list of company join requests."""
        self.create_user_request()
        query_params = {'company_id': self.company['id']}
        url = reverse('request_list')
        response = self.client.get(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_approve_request(self):
        """Test approving a company join request."""
        user_request = self.create_user_request()
        query_params = {'company_id': self.company['id'], 'status': RequestStatusEnum.APPROVED.value}
        url = reverse('request_action', args=[user_request.data['id']])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], RequestStatusEnum.APPROVED.value)

    def test_reject_request(self):
        """Test rejecting a company join request."""
        user_request = self.create_user_request()
        query_params = {'company_id': self.company['id'], 'status': RequestStatusEnum.REJECTED.value}
        url = reverse('request_action', args=[user_request.data['id']])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], RequestStatusEnum.REJECTED.value)


class UserRequestActionsViewTestCase(BaseTestCase):
    """Test case for the UserRequestActionsView, which handles various user request and invitation actions."""

    def setUp(self):
        super().setUp()
        self._authentication(self.member_token)

    def create_user_request(self, company_id):
        """Create a user request to join a company."""
        query_params = {'company_id': company_id}
        url = reverse('user_request_list')
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        return response

    def test_create_user_request(self):
        """Test the creation of a user request to join a company."""
        request_count = RequestModel.objects.count()
        employee_count = EmployeeModel.objects.count()
        user_request = self.create_user_request(company_id=self.company['id'])

        self.assertEqual(user_request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(RequestModel.objects.count(), request_count + 1)
        self.assertEqual(user_request.data['status'], RequestStatusEnum.PENDING.value)

    def test_get_user_request_list(self):
        """Test retrieving a list of user join requests."""
        self.create_user_request(company_id=self.company['id'])

        response = self.client.get(reverse('user_request_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_cancel_request(self):
        """Test canceling a user's request."""
        user_request = self.create_user_request(company_id=self.company['id'])
        url = reverse('user_request_action', args=[user_request.data['id']])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], RequestStatusEnum.CANCELED.value)


class UserInviteActionsViewTestCase(BaseTestCase):
    """Test case for the UserRequestActionsView, which handles various user request and invitation actions."""

    def setUp(self):
        super().setUp()
        self._authentication(self.member_token)

    def test_get_user_invite_list(self):
        """Test retrieving a list of user invitations."""
        self.create_company_invite(self.member_token)
        url = reverse('user_invites_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_accept_invite(self):
        """Test accepting a user invitation."""
        invite = self.create_company_invite(self.member_token)
        query_params = {"status": InviteStatusEnum.ACCEPTED.value}
        url = reverse('user_invites_action', args=[invite.data['id']])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], InviteStatusEnum.ACCEPTED.value)

    def test_decline_invite(self):
        """Test declining a user invitation."""
        invite = self.create_company_invite(self.member_token)
        query_params = {"status": InviteStatusEnum.DECLINED.value}
        url = reverse('user_invites_action', args=[invite.data['id']])
        response = self.client.patch(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], InviteStatusEnum.DECLINED.value)
