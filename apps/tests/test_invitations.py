from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.companies.employee.models import EmployeeModel
from apps.companies.models import CompanyModel
from apps.invitations.models import InviteModel, RequestModel
from apps.users.models import UserModel as User
from core.enums.constants_enum import ConstantsEnum
from core.enums.invite_enum import InviteEnum
from core.enums.request_enum import RequestEnum
from core.enums.user_enum import UserEnum

UserModel: User = get_user_model()


class CompanyInviteActionsViewTestCase(APITestCase):

    def setUp(self):
        self.user_owner = UserModel.objects.create_user(email="testuser@example.com", password="P@$$word1")
        self.member_user = User.objects.create_user(email='member_user@example.com', password='P@$$word1')
        self.company = CompanyModel.objects.create(name="Test Company", description="Test description")
        self.employee = EmployeeModel.objects.create(user=self.user_owner, company=self.company,
                                                     role=UserEnum.OWNER.value)

        self.token = self.client.post(reverse("jwt-create"), {
            "email": "testuser@example.com",
            "password": "P@$$word1"
        })


    def test_create_company_invite(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        invite_count = InviteModel.objects.count()
        employee_count = EmployeeModel.objects.count()

        data = {'user': self.member_user.id, 'status': InviteEnum.PENDING}
        url = reverse('invitation_action', args=[self.company.id])
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(InviteModel.objects.count(), invite_count + 1)

    def test_get_company_invites_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])

        invite = InviteModel.objects.create(user=self.member_user, company=self.company, status=InviteEnum.PENDING)
        EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.CANDIDATE.value,
                                     invite_status=invite)

        invite_data = {"invitation_status": "invite"}
        url = reverse('invitation_action', args=[self.company.id])
        response = self.client.get(url, invite_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)


    def test_get_company_request_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        user_request = RequestModel.objects.create(user=self.member_user, company=self.company,
                                                   status=RequestEnum.PENDING)
        EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.CANDIDATE.value,
                                     request_status=user_request)
        data = {"invitation_status": ConstantsEnum.REQUEST.value}
        url = reverse('invitation_action', args=[self.company.id])
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_revoke_invite(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        invite = InviteModel.objects.create(user=self.member_user, company=self.company,
                                            status=InviteEnum.PENDING.value)
        EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.CANDIDATE.value,
                                     invite_status=invite)
        data = {
            "user_id": self.member_user.id,
            "invitation_status": InviteEnum.REVOKE.value
        }
        url = reverse('invitation_action', args=[self.company.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)

    def test_approve_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        user_request = RequestModel.objects.create(user=self.member_user, company=self.company,
                                                   status=RequestEnum.PENDING.value)
        EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.CANDIDATE.value,
                                     request_status=user_request)
        data = {
            "user_id": self.member_user.id,
            "invitation_status": RequestEnum.APPROVE.value
        }
        url = reverse('invitation_action', args=[self.company.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], UserEnum.MEMBER.value)

    def test_reject_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        user_request = RequestModel.objects.create(user=self.member_user, company=self.company,
                                                   status=RequestEnum.PENDING.value)
        EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.CANDIDATE.value,
                                     request_status=user_request)
        data = {
            "user_id": self.member_user.id,
            "invitation_status": RequestEnum.REJECTED.value
        }
        url = reverse('invitation_action', args=[self.company.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)


class UserRequestActionsViewTestCase(APITestCase):
    def setUp(self):
        self.user_owner = UserModel.objects.create_user(email="testuser@example.com", password="P@$$word1")
        self.member_user = User.objects.create_user(email='member_user@example.com', password='P@$$word1')
        self.company = CompanyModel.objects.create(name="Test Company", description="Test description")
        self.employee = EmployeeModel.objects.create(user=self.user_owner, company=self.company,
                                                     role=UserEnum.OWNER.value)

        self.token = self.client.post(reverse("jwt-create"), {
            "email": "member_user@example.com",
            "password": "P@$$word1"
        })

    def test_create_user_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        request_count = RequestModel.objects.count()
        employee_count = EmployeeModel.objects.count()

        url = reverse('request_create_actions', args=[self.company.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeModel.objects.count(), employee_count + 1)
        self.assertEqual(RequestModel.objects.count(), request_count + 1)
        self.assertEqual(response.data['status'], RequestEnum.PENDING.value)

    def test_get_user_request_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        user_request = RequestModel.objects.create(user=self.member_user, company=self.company,
                                                   status=RequestEnum.PENDING.value)
        EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.CANDIDATE.value,
                                     request_status=user_request)
        data = {"invitation_status": ConstantsEnum.REQUEST.value}
        url = reverse('request_list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_get_user_invite_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        user_invite = InviteModel.objects.create(user=self.member_user, company=self.company,
                                                 status=RequestEnum.PENDING)
        EmployeeModel.objects.create(user=self.member_user, company=self.company, role=UserEnum.CANDIDATE.value,
                                     invite_status=user_invite)

        data = {"invitation_status": ConstantsEnum.INVITE.value}
        url = reverse('request_list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_cancel_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        user_request = RequestModel.objects.create(user=self.member_user, company=self.company,
                                                   status=RequestEnum.PENDING.value)
        employee = EmployeeModel.objects.create(user=self.member_user, company=self.company,
                                                role=UserEnum.CANDIDATE.value,
                                                request_status=user_request)
        data = {"invitation_status": RequestEnum.CANCEL.value}

        url = reverse('request_detail_actions', args=[employee.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)

    def test_accept_invite(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        invite = InviteModel.objects.create(user=self.member_user, company=self.company,
                                            status=InviteEnum.PENDING.value)
        employee = EmployeeModel.objects.create(user=self.member_user, company=self.company,
                                                role=UserEnum.CANDIDATE.value, invite_status=invite)
        data = {"invitation_status": InviteEnum.ACCEPT.value}

        url = reverse('request_detail_actions', args=[employee.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], UserEnum.MEMBER.value)

    def test_decline_invite(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        invite = InviteModel.objects.create(user=self.member_user, company=self.company,
                                            status=InviteEnum.PENDING.value)
        employee = EmployeeModel.objects.create(user=self.member_user, company=self.company,
                                                role=UserEnum.CANDIDATE.value, invite_status=invite)
        data = {"invitation_status": InviteEnum.DECLINE.value}

        url = reverse('request_detail_actions', args=[employee.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], None)
