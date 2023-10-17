from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.helper import get_user_role_in_company
from apps.companies.models import CompanyModel
from apps.companies.serializers import (
    EmployeeSerializer,
)
from apps.invitations.models import EmployeeModel
from apps.invitations.serializers import EmployeeListSerializer
from apps.users.models import UserModel as User
from core.enums.invitation_enum import InvitationEnum
from core.enums.user_enum import UserEnum
from core.permisions.is_company_invite_owner import IsCompanyInviteOwnerPermission
from core.permisions.is_company_owner import IsCompanyOwnerPermission

UserModel: User = get_user_model()


class InviteView(ListCreateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = EmployeeSerializer
    serializer_class_list = EmployeeListSerializer
    permission_classes = (IsAuthenticated, IsCompanyOwnerPermission)

    def get_serializer_class(self):

        if self.request.method in ['POST']:
            return self.serializer_class
        return self.serializer_class_list

    def create(self, request, *args, **kwargs):
        user_id = request.query_params.get('candidate_id')
        company = self.get_object()

        if company.has_member(user_id):
            return Response({'detail': 'Candidate have already relation to this company'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializers_data = {
            "user": user_id,
            "company": company.id,
            "invitation_status": InvitationEnum.PENDING,
            "role": UserEnum.CANDIDATE
        }
        serializer = self.get_serializer(data=serializers_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        invitation_action, = self.request.query_params.keys()
        company = self.get_object()

        if self.request.query_params[invitation_action] == 'invite':
            candidates = EmployeeModel.objects.filter(company=company, invitation_status=InvitationEnum.PENDING)
        else:
            if self.request.query_params[invitation_action] == 'members':
                candidates = EmployeeModel.objects.filter(company=company, role__in=[UserEnum.MEMBER, UserEnum.OWNER])
            else:
                candidates = EmployeeModel.objects.filter(company=company, request_status=InvitationEnum.PENDING)

        page = self.paginate_queryset(candidates)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class InviteActionView(RetrieveUpdateDestroyAPIView):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyInviteOwnerPermission]

    def destroy(self, request, *args, **kwargs):
        employee = self.get_object()
        employee.invitation_status = 'cancel'
        employee.role = UserEnum.FORMER
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class RequestView(CreateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        company = self.get_object()

        if company.has_member(request.user):
            return Response({'detail': 'You have already relation to this company'}, status=status.HTTP_400_BAD_REQUEST)

        serializers_data = {
            "user": request.user.id,
            "company": company.id,
            "request_status": InvitationEnum.PENDING,
            "role": UserEnum.CANDIDATE
        }
        serializer = self.get_serializer(data=serializers_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RequestActionView(ListAPIView, RetrieveUpdateDestroyAPIView):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if 'pk' in self.kwargs:
            employee = get_object_or_404(self.queryset, pk='pk', user=self.request.user.id)
            serializer = self.serializer_class(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            key, = self.request.query_params.keys()
            if key == 'request_status':
                queryset = EmployeeModel.objects.filter(user=self.request.user.id,
                                                        request_status=self.request.query_params[key])
            else:
                queryset = EmployeeModel.objects.filter(user=self.request.user.id,
                                                        invitation_status=self.request.query_params[key])

            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def patch(self, request, *args, **kwargs):
        key, = self.request.query_params.keys()
        if key == 'request_action':

            employee = get_object_or_404(self.queryset, pk='pk')
            role = get_user_role_in_company(self.request.user.id, employee.company_id)

            if role != UserEnum.OWNER:
                return Response({'message': 'You are not the owner of this company'}, status=status.HTTP_403_FORBIDDEN)

            if self.request.query_params[key] == InvitationEnum.ACCEPTED:
                employee.request_status = InvitationEnum.ACCEPTED
                employee.role = UserEnum.MEMBER
            else:
                employee.invitation_status = InvitationEnum.REJECTED

        else:
            employee = get_object_or_404(self.queryset, pk='pk', user=self.request.user.id)

            if self.request.query_params[key] == InvitationEnum.ACCEPTED:
                employee.invitation_status = InvitationEnum.ACCEPTED
                employee.role = UserEnum.MEMBER
            else:
                employee.invitation_status = InvitationEnum.REJECTED

        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        employee = get_object_or_404(self.queryset, pk='pk', user=self.request.user.id)
        if employee.request_status in ['pending', 'accepted']:
            employee.request_status = 'cancel'
            employee.role = UserEnum.FORMER
            employee.save()
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={"detail": "You don't have permission."},
                status=status.HTTP_400_BAD_REQUEST
            )


class LeaveCompanyView(DestroyAPIView):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        company_id = kwargs.get('pk')

        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            employee = get_object_or_404(EmployeeModel, user=user_id, company__id=company_id, role='member')
            if not employee.company.is_owner(request.user):
                return Response({"detail": "Only owners can remove users from the company."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            employee = get_object_or_404(EmployeeModel, user=request.user, company__id=company_id, role='member')

            if employee.company.is_owner(request.user):
                return Response({"detail": "Owners cannot leave the company."}, status=status.HTTP_400_BAD_REQUEST)
        if employee.request_status:
            employee.request_status = 'cancel'
        else:
            employee.invitation_status = 'cancel'
        employee.role = UserEnum.FORMER
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
