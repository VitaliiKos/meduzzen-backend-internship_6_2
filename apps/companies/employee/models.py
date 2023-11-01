from django.contrib.auth import get_user_model
from django.db import models

from apps.companies.models import CompanyModel
from apps.health_check.models import TimeStampedModel
from apps.invitations.models import InviteModel, RequestModel
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
    role = models.CharField(max_length=255, choices=[(role.value, role) for role in UserEnum], null=True)

    invite_status = models.ForeignKey(InviteModel, on_delete=models.CASCADE, null=True, blank=True)
    request_status = models.ForeignKey(RequestModel, on_delete=models.CASCADE, null=True, blank=True)

    def toggle_employee_role(self, new_role):
        role_mapping = {
            UserEnum.MEMBER.value: UserEnum.ADMIN.value,
            UserEnum.ADMIN.value: UserEnum.MEMBER.value
        }
        old_role = role_mapping.get(new_role)
        if self.role == old_role:
            self.role = new_role
            self.save()
            return True

