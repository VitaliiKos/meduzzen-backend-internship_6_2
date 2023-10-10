from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

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
        serializer.save(members=self.request.user)


class UserRelatedCompaniesListView(ListAPIView):
    """List companies owned or joined by the current user."""

    serializer_class = CompaniesForCurrentUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return CompanyModel.objects.filter(members=user)


class CompanyRetrieveUpdateDestroyView(ListAPIView, RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a company."""

    queryset = CompanyModel.objects.all()
    serializer_class = CompaniesForCurrentUserSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_destroy(self, instance):
        serializer = self.get_serializer(instance)
        serializer.delete_company(instance, user_id=self.request.user.id)

