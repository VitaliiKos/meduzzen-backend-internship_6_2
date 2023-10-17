from django.contrib.auth import get_user_model
from django.db import models

from apps.companies.models import CompanyModel
from apps.health_check.models import TimeStampedModel
from core.enums.invitation_enum import InvitationEnum
from core.enums.user_enum import UserEnum

UserModel = get_user_model()


class EmployeeModel(TimeStampedModel):
    """Model representing an employee's relationship with a company.

    This model defines the relationship between users and companies,
    including their invitation status, request status, and role.
    """

    class Meta:
        db_table = 'employee'
        ordering = ('-created_at',)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)

    invitation_status = models.CharField(max_length=10, choices=[(status.value, status) for status in InvitationEnum],
                                         default=None, null=True)
    request_status = models.CharField(max_length=10, choices=[(status.value, status) for status in InvitationEnum],
                                      default=None, null=True)
    role = models.CharField(max_length=255, choices=[(role.value, role) for role in UserEnum], null=False)
