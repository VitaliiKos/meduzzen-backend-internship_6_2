from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from core.enums.company_helper_enum import CompanyHelperEnum
from core.permisions.company_permission import IsCompanyOwnerOrReadOnly

from .models import CompanyModel
from .models import UserModel as User
from .serializers import CompaniesForCurrentUserSerializer, CompanySerializer

UserModel: User = get_user_model()


class CompanyView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    """Create, retrieve, update, or delete a company."""
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
    serializer_class_for_current_user = CompaniesForCurrentUserSerializer
    permission_classes = (IsAuthenticated, IsCompanyOwnerOrReadOnly)

    def get_serializer_class(self):

        if CompanyHelperEnum.OPTION in self.request.query_params or self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return self.serializer_class_for_current_user
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        if self.get_serializer_class() == CompaniesForCurrentUserSerializer and 'pk' not in self.kwargs:
            queryset = CompanyModel.objects.filter(members=user)
        else:
            queryset = CompanyModel.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):

        if 'pk' in self.kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(members=self.request.user)
