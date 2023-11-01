from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from apps.users.models import UserModel as User

fake = Faker()
UserModel: User = get_user_model()


class BaseTestCase(APITestCase):
    """Base test case for common setup and utility functions."""

    fixtures = ["apps/companies/tests/fixtures/company_model_fixture",
                "apps/companies/employee/tests/fixtures/employee_model_fixture",
                "apps/invitations/tests/fixtures/invite_model_fixture.json",
                "apps/invitations/tests/fixtures/request_model_fixture",
                "apps/users/tests/fixtures/users_model_fixture"]

    def _authentication(self, user):
        """Set the authentication credentials using the provided token."""
        self.client.force_authenticate(user=user)


class BaseInvitationTestCase(APITestCase):
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
