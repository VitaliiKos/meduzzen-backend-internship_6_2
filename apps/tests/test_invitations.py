from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.companies.employee.models import EmployeeModel
from apps.invitations.models import InviteModel, RequestModel
from apps.users.models import UserModel as User
from core.enums.constants_enum import ConstantsEnum
from core.enums.invite_enum import InviteEnum
from core.enums.request_enum import RequestEnum
from core.enums.user_enum import UserEnum

fake = Faker()
UserModel: User = get_user_model()


def generate_user_info():
    """Generate user data for new user."""
    password = fake.password()
    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": password,
        "re_password": password,
    }
    return data


class CompanyInviteActionsViewTestCase(APITestCase):
    """Test case for the CompanyInviteActionsView, which handles various company invite and request actions."""

    def setUp(self):
        """Test case for the CompanyInviteActionsView, which handles various company invite and request actions."""
        self.owner_user_info = generate_user_info()
        self.member_user_info = generate_user_info()
        self.owner = self.client.post(reverse("usermodel-list"), self.owner_user_info)
        self.member = self.client.post(reverse("usermodel-list"), self.member_user_info)

        self.member_token = self.get_token(self.member_user_info)

        self.owner_token = self.get_token(self.owner_user_info)
        self.company = self.create_company()

    def create_company(self):
        """Create a company with the owner's credentials."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)

        data = {
            "name": fake.company(),
            "description": fake.text(max_nb_chars=50),
            "visible": True,
        }
        url = reverse('company_list')
        response = self.client.post(url, data)
        return response.data

    def get_token(self, user):
        """Retrieve a JWT token for a given user."""
        data = {
            "email": user["email"],
            "password": user['password'],
        }
        token = self.client.post(reverse("jwt-create"), data)
        return token.data['access']

    def create_user_request(self):
        """Create a user request to join a company."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        request_count = RequestModel.objects.count()
        employee_count = EmployeeModel.objects.count()
        data = {'user': self.member.data['id']}
        url = reverse('request_create_actions', args=[self.company['id']])
        response = self.client.post(url, data)

        self.assertEqual(response.data['status'], InviteEnum.PENDING.value)
        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RequestModel.objects.count(), request_count + 1)

    def test_create_company_invite(self):
        """Test the creation of a company invite."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        invite_count = InviteModel.objects.count()
        employee_count = EmployeeModel.objects.count()

        data = {'user': self.member.data['id']}
        url = reverse('invitation_action', args=[self.company['id']])
        response = self.client.post(url, data, format='json')

        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(InviteModel.objects.count(), invite_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], InviteEnum.PENDING.value)

    def test_get_company_invites_list(self):
        """Test retrieving a list of company invites."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        self.test_create_company_invite()

        invite_data = {"invitation_status": "invite"}
        url = reverse('invitation_action', args=[self.company['id']])
        response = self.client.get(url, invite_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_get_company_request_list(self):
        """Test retrieving a list of company join requests."""
        self.create_user_request()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)

        data = {"invitation_status": ConstantsEnum.REQUEST.value}
        url = reverse('invitation_action', args=[self.company['id']])
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_revoke_invite(self):
        """Test revoking a company invite."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        self.test_create_company_invite()

        data = {
            "user_id": self.member.data['id'],
            "invitation_status": InviteEnum.REVOKED.value
        }
        url = reverse('invitation_action', args=[self.company['id']])
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)

    def test_approve_request(self):
        """Test approving a company join request."""
        self.create_user_request()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        data = {
            "invitation_status": RequestEnum.APPROVED.value,
            "user_id": self.member.data['id']
        }
        url = reverse('invitation_action', args=[self.company['id']])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], UserEnum.MEMBER.value)

    def test_reject_request(self):
        """Test rejecting a company join request."""
        self.create_user_request()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        data = {
            "invitation_status": RequestEnum.REJECTED.value,
            "user_id": self.member.data['id']
        }
        url = reverse('invitation_action', args=[self.company['id']])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)


class UserRequestActionsViewTestCase(APITestCase):
    """Test case for the UserRequestActionsView, which handles various user request and invitation actions."""

    def setUp(self):
        """Set up method which is used to initialize before any test run."""
        self.owner_user_info = generate_user_info()
        self.member_user_info = generate_user_info()
        self.owner = self.client.post(reverse("usermodel-list"), self.owner_user_info)
        self.member = self.client.post(reverse("usermodel-list"), self.member_user_info)

        self.member_token = self.get_token(self.member_user_info)

        self.owner_token = self.get_token(self.owner_user_info)
        self.company = self.create_company()

    def get_token(self, user):
        """Retrieve a JWT token for a given user."""
        data = {
            "email": user["email"],
            "password": user['password'],
        }
        token = self.client.post(reverse("jwt-create"), data)
        return token.data['access']

    def create_company_invite(self):
        """Create a company invite."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        invite_count = InviteModel.objects.count()
        employee_count = EmployeeModel.objects.count()
        url = reverse('invitation_action', args=[self.company['id']])
        response = self.client.post(url, {'user': self.member.data['id']})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], InviteEnum.PENDING.value)
        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(InviteModel.objects.count(), invite_count + 1)

    def create_user_request(self, company_id):
        """Create a user request to join a company."""
        url = reverse('request_create_actions', args=[company_id])
        response = self.client.post(url)
        return response

    def create_company(self):
        """Create a company with the owner's credentials."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)

        data = {
            "name": fake.company(),
            "description": fake.text(max_nb_chars=50),
            "visible": True,
        }
        url = reverse('company_list')
        response = self.client.post(url, data)
        return response.data

    def test_create_user_request(self):
        """Test the creation of a user request to join a company."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        request_count = RequestModel.objects.count()
        employee_count = EmployeeModel.objects.count()
        user_request = self.create_user_request(company_id=self.company['id'])

        self.assertEqual(user_request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(RequestModel.objects.count(), request_count + 1)
        self.assertEqual(user_request.data['status'], RequestEnum.PENDING.value)

    def test_get_user_request_list(self):
        """Test retrieving a list of user join requests."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        self.create_user_request(company_id=self.company['id'])

        data = {"invitation_status": ConstantsEnum.REQUEST.value}
        response = self.client.get(reverse('request_list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_get_user_invite_list(self):
        """Test retrieving a list of user invitations."""
        self.create_company_invite()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)

        data = {"invitation_status": ConstantsEnum.INVITE}
        url = reverse('request_list')
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_cancel_request(self):
        """Test canceling a user's request."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        self.test_create_user_request()
        user_request = EmployeeModel.objects.get(user=self.member.data['id'],
                                                 role=UserEnum.CANDIDATE,
                                                 request_status__isnull=False)
        data = {"invitation_status": RequestEnum.CANCELED.value}

        url = reverse('request_detail_actions', args=[user_request.id])
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)
        self.assertEqual(RequestModel.objects.get(id=user_request.request_status_id).status, RequestEnum.CANCELED.value)

    def test_accept_invite(self):
        """Test accepting a user invitation."""
        self.create_company_invite()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        user_invite = EmployeeModel.objects.get(user=self.member.data['id'], role=UserEnum.CANDIDATE,
                                                invite_status__isnull=False)

        data = {"invitation_status": InviteEnum.ACCEPTED.value}

        url = reverse('request_detail_actions', args=[user_invite.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], UserEnum.MEMBER.value)
        self.assertEqual(InviteModel.objects.get(id=user_invite.invite_status_id).status, InviteEnum.ACCEPTED.value)

    def test_decline_invite(self):
        """Test declining a user invitation."""
        self.create_company_invite()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        user_invite = EmployeeModel.objects.get(user=self.member.data['id'], role=UserEnum.CANDIDATE,
                                                invite_status__isnull=False)

        data = {"invitation_status": InviteEnum.DECLINED.value}

        url = reverse('request_detail_actions', args=[user_invite.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)
        self.assertEqual(InviteModel.objects.get(id=user_invite.invite_status_id).status, InviteEnum.DECLINED.value)
