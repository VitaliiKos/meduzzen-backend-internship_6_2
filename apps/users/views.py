from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView, UpdateAPIView
import logging
from .models import UserModel as User, ProfileModel
from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
UserModel: User = get_user_model()


class UsersListCreateView(ListCreateAPIView):
    logger.info('Information incoming!')
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer


class UserProfileUpdateView(UpdateAPIView):
    logger.info('Information incoming!')
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer


class UserRetrieveUpdateDestroyView(RetrieveDestroyAPIView):
    logger.info('Information incoming!')
    queryset = User.objects.all()
    serializer_class = UserSerializer

