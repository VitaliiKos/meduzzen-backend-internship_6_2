from rest_framework.serializers import ModelSerializer

from apps.companies.employee.models import EmployeeModel
from apps.invitations.serializers import InviteModelSerializer
from apps.users.serializers import UserSerializer


class EmployeeSerializer(ModelSerializer):
    """Serializer for EmployeeModel objects."""

    class Meta:
        model = EmployeeModel
        order_by = ('created_at',)
        fields = '__all__'


class EmployeeListSerializer(ModelSerializer):
    """Serializer for EmployeeModel objects."""
    user = UserSerializer()
    invite_status = InviteModelSerializer()

    class Meta:
        model = EmployeeModel
        order_by = ('created_at',)
        fields = ('id', 'user', 'company', 'invite_status', 'request_status', 'role', 'created_at')
