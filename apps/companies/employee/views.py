from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.employee.models import EmployeeModel
from apps.companies.employee.serializers import EmployeeListSerializer, EmployeeSerializer
from apps.companies.models import CompanyModel
from core.enums.user_enum import UserEnum
from core.permisions.company_permission import IsCompanyOwner, IsOwnerReadOnly


class EmployeeActionView(ListAPIView, RetrieveUpdateAPIView):
    """API endpoint for managing employees within a company.

    - Only the owner of the company can retrieve the list of employees.
    - Only the owner of the company can remove an employee.
    - Employees can leave the company themselves.
    """

    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)

    def get_queryset(self):
        company_id = self.request.query_params.get('company_id')
        company = CompanyModel.objects.get(id=company_id)
        return company.get_members()

    def update(self, request, *args, **kwargs):
        company_id = self.request.query_params.get('company_id')
        user_id = self.request.query_params.get('user_id', None)
        company = get_object_or_404(CompanyModel, id=company_id)

        if user_id and company.is_owner(request.user):
            user_to_leave = user_id
        elif not user_id and not company.is_owner(request.user):
            user_to_leave = request.user.id
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        employee = get_object_or_404(EmployeeModel, user=user_to_leave, company=company,
                                     role__in=[UserEnum.MEMBER.value, UserEnum.ADMIN.value])
        employee.role = None
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class AdminActionView(ListAPIView, UpdateAPIView):
    """API for managing employee roles within a company.
    - List and update admin/member roles of employees.
    - Only the owner of the company can change an employee's role from 'member' to 'admin' or vice versa.
    """

    serializer_class = EmployeeListSerializer
    permission_classes = (IsAuthenticated, IsCompanyOwner)

    def get_queryset(self):
        company_id = self.request.query_params.get('company_id')
        company = CompanyModel.objects.get(id=company_id)
        return company.get_admins()

    def patch(self, request, *args, **kwargs):
        new_role = self.request.query_params.get('role')
        member_id = self.request.query_params.get('user_id')
        company_id = self.request.query_params.get('company_id')
        company = get_object_or_404(CompanyModel, id=company_id)

        employee = get_object_or_404(EmployeeModel, user=member_id, company=company)

        if employee.change_employee_role(new_role):
            serializer = self.serializer_class(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Incorrect role or employee does not have the specified role."},
                            status=status.HTTP_400_BAD_REQUEST)
