from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView, UpdateAPIView
import logging
from .models import UserModel as User, ProfileModel
from .serializers import UserAccountSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)
UserModel: User = get_user_model()


class UsersListCreateView(ListCreateAPIView):
    logger.info('Information incoming!')
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = (AllowAny,)


class UserProfileUpdateView(UpdateAPIView):
    logger.info('Information incoming!')
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateDestroyView(RetrieveDestroyAPIView):
    logger.info('Information incoming!')
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = (AllowAny,)
