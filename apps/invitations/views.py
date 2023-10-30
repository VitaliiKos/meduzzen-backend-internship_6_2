from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.employee.models import EmployeeModel
from apps.companies.models import CompanyModel
from apps.invitations.helper import select_role, update_employee
from apps.invitations.models import InviteModel, RequestModel
from apps.invitations.serializers import InviteModelSerializer, RequestModelSerializer
from apps.users.models import UserModel as User
from core.enums.invite_enum import InviteStatusEnum
from core.enums.request_enum import RequestStatusEnum
from core.permisions.company_permission import IsCompanyInvitationOwner

UserModel: User = get_user_model()


class CompanyInviteActionsView(ListCreateAPIView, RetrieveUpdateAPIView):
    """A view for handling company invitations."""
    serializer_class = InviteModelSerializer
    permission_classes = (IsAuthenticated, IsCompanyInvitationOwner)

    def get_queryset(self):
        company_id = self.request.query_params.get('company_id')
        if not company_id:
            queryset = InviteModel.objects.all()
        else:
            queryset = InviteModel.objects.filter(company=company_id, status=InviteStatusEnum.PENDING)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a company invitation."""
        user_id = self.request.query_params.get('user_id')
        company_id = self.request.query_params.get('company_id')
        company = get_object_or_404(CompanyModel, id=company_id)

        if company.has_member(user_id):
            return Response({'detail': 'Candidate have already relation to this company'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializers_data = {
            "user": user_id,
            "company": company.id,
            "status": InviteStatusEnum.PENDING,
        }
        serializer = self.get_serializer(data=serializers_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Revoke a company invitation."""
        invite = self.get_object()
        employee = get_object_or_404(EmployeeModel, invite_status_id=invite.id,
                                     invite_status__status=InviteStatusEnum.PENDING.value)

        updated_invite = update_employee(employee, InviteStatusEnum.REVOKED.value, invite)

        serializer = InviteModelSerializer(updated_invite)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyRequestActionsView(ListAPIView, RetrieveUpdateAPIView):
    """A view for handling company requests."""
    serializer_class = RequestModelSerializer
    permission_classes = (IsAuthenticated, IsCompanyInvitationOwner)

    def get_queryset(self):
        company_id = self.request.query_params.get('company_id')
        queryset = RequestModel.objects.filter(company=company_id, status=RequestStatusEnum.PENDING)
        return queryset

    def update(self, request, *args, **kwargs):
        """Approve or reject a company request."""
        user_request = self.get_object()
        new_request_status = self.request.query_params.get('status')
        employee = get_object_or_404(EmployeeModel, request_status_id=user_request.id)
        role = select_role(new_request_status)

        updated_request = update_employee(employee, new_request_status, user_request, role)

        serializer = self.serializer_class(updated_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRequestActionsView(ListCreateAPIView, RetrieveUpdateAPIView):
    """A view for handling user requests to join a company."""
    serializer_class = RequestModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = RequestModel.objects.filter(user=self.request.user, status=RequestStatusEnum.PENDING)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a user request to join a company."""
        user = self.request.user.id
        company_id = self.request.query_params.get('company_id')
        company = get_object_or_404(CompanyModel, id=company_id)
        if company.has_member(user):
            return Response({'detail': 'Candidate have already relation to this company'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializers_data = {
            "user": user,
            "company": company.id,
            "status": RequestStatusEnum.PENDING
        }
        serializer = self.get_serializer(data=serializers_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Cancel a user's request."""

        user_request = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        employee = get_object_or_404(EmployeeModel, request_status=user_request.id)

        updated_request = update_employee(employee, RequestStatusEnum.CANCELED.value, user_request)

        serializer = InviteModelSerializer(updated_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserInviteActionView(ListAPIView, RetrieveUpdateAPIView):
    """A view for handling user invitation details and responses."""
    serializer_class = InviteModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = InviteModel.objects.filter(user=self.request.user.id, status=InviteStatusEnum.PENDING.value)
        return queryset

    def update(self, request, *args, **kwargs):
        """Accept or decline invite."""
        new_request_status = self.request.query_params.get('status')
        invite = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        employee = get_object_or_404(EmployeeModel, invite_status=invite.id)
        role = select_role(new_request_status)

        updated_request = update_employee(employee, new_request_status, invite, role)

        serializer = self.serializer_class(updated_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
