from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.check_is_owner import get_user_role_in_company

from .models import CompanyModel
from .models import UserModel as User
from .serializers import CompaniesForCurrentUserSerializer, CompanySerializer

UserModel: User = get_user_model()


class CompanyListCreateView(ListCreateAPIView):
    """List and create companies."""

    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
    permission_classes = IsAuthenticated,

    def perform_create(self, serializer):
        """Create a new company.

        This method is called when creating a new company.
        It associates the current user as a member of the company.
        """
        serializer.save(members=self.request.user)


class MyCompaniesView(ListCreateAPIView):
    """List companies for the current user."""

    serializer_class = CompaniesForCurrentUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Get the list of companies for the current user."""
        user = self.request.user
        return CompanyModel.objects.filter(members=user)


class CompanyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a company.

    This view allows users to retrieve, update, or delete a company
    if they have the necessary permissions.
    """

    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        """Update a company.

        This method updates the details of a company if the user has permission.
        """
        company = self.get_object()
        current_user = self.request.user

        member_role = get_user_role_in_company(user_id=current_user.id, company_id=company.id)

        if not member_role:
            return Response({'detail': 'You do not have permission to update this company.'},
                            status=status.HTTP_400_BAD_REQUEST)

        company.name = request.data.get('name', company.name)
        company.description = request.data.get('description', company.description)
        company.status = request.data.get('status', company.status)
        company.save()
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """Toggle the status of a company.

        This method toggles the status of a company if the user has permission.
        """
        company = self.get_object()
        current_user = self.request.user

        member_role = get_user_role_in_company(user_id=current_user.id, company_id=company.id)

        if not member_role:
            return Response({'detail': 'You do not have permission to update this company.'},
                            status=status.HTTP_400_BAD_REQUEST)

        company.status = not company.status
        company.save()
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Delete a company.

        This method deletes a company if the user has permission.
        """
        company = self.get_object()
        current_user = self.request.user
        member_role = get_user_role_in_company(user_id=current_user.id, company_id=company.id)
        if not member_role:
            return Response({'detail': 'You do not have permission to update this company.'},
                            status=status.HTTP_400_BAD_REQUEST)

        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
