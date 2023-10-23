from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.employee.models import EmployeeModel
from apps.companies.employee.serializers import EmployeeListSerializer, EmployeeSerializer
from apps.companies.models import CompanyModel
from core.enums.user_enum import UserEnum
from core.permisions.IsOwnerOrReadOnly import IsOwnerOrReadOnly


class EmployeeActionView(ListAPIView, RetrieveUpdateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def list(self, request, *args, **kwargs):
        company = self.get_object()

        employees = EmployeeModel.objects.filter(company=company, role__in=[UserEnum.OWNER, UserEnum.MEMBER])

        page = self.paginate_queryset(employees)
        serializer = EmployeeListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        company = get_object_or_404(self.queryset, pk=kwargs['pk'])
        user_id = request.data.get('user_id')

        if user_id is not None:

            if not company.is_owner(request.user):
                raise PermissionDenied("Only owners can remove users from the company.")

            employee = get_object_or_404(EmployeeModel, user=user_id, company=company, role='member')
        else:
            employee = get_object_or_404(EmployeeModel, user=request.user, company__id=company.id, role='member')

            if employee.company.is_owner(request.user):
                raise PermissionDenied("Owners cannot leave the company.")

        employee.role = None
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
