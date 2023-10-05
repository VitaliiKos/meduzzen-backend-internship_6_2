import logging

from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from .models import ProfileModel
from .models import UserModel as User
from .serializers import ProfileSerializer, UserAccountSerializer

logger = logging.getLogger(__name__)
UserModel: User = get_user_model()


class UsersListCreateView(ListCreateAPIView):
    """API view for listing and creating users."""

    logger.info('Information incoming!')
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = (AllowAny,)


class UserProfileUpdateView(UpdateAPIView):
    """API view for updating user profiles."""

    logger.info('Information incoming!')
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateDestroyView(RetrieveDestroyAPIView):
    """API view for retrieving, updating, and destroying user accounts."""

    logger.info('Information incoming!')
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = (AllowAny,)
