from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.employee.models import EmployeeModel
from apps.companies.employee.serializers import EmployeeListSerializer, EmployeeSerializer
from apps.companies.models import CompanyModel
from core.enums.user_enum import UserEnum
from core.permisions.company_permission import IsOwnerReadOnly


class EmployeeActionView(ListAPIView, RetrieveUpdateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)

    def list(self, request, *args, **kwargs):
        company = self.get_object()
        members = company.get_members()

        page = self.paginate_queryset(members)
        serializer = EmployeeListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        company = get_object_or_404(self.queryset, pk=kwargs['pk'])
        user_id = request.data.get('user_id')

        if user_id and company.is_owner(request.user):
            user_to_leave = user_id
        elif not user_id and not company.is_owner(request.user):
            user_to_leave = request.user.id
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        employee = get_object_or_404(EmployeeModel, user=user_to_leave, company=company, role=UserEnum.MEMBER)
        employee.role = None
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
