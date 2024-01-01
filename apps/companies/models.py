from django.contrib.auth import get_user_model
from django.db import models

from apps.health_check.models import TimeStampedModel
from core.enums.user_enum import UserEnum

UserModel = get_user_model()


class CompanyModel(TimeStampedModel):
    """Model representing a company."""

    class Meta:
        db_table = 'company'
        ordering = ('created_at',)

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    visible = models.BooleanField(default=False)

    members = models.ManyToManyField(UserModel, through="employee.EmployeeModel")

    def is_owner(self, user):
        return self.employeemodel_set.filter(user=user, role=UserEnum.OWNER).exists()

    def is_admin(self, user):
        return self.employeemodel_set.filter(user=user, role=UserEnum.OWNER).exists()

    def has_member(self, user):
        return self.employeemodel_set.filter(user=user, role__isnull=False).exists()

    def get_members(self):
        """Get all employees with roles 'OWNER' or 'MEMBER' for this company."""
        return self.employeemodel_set.filter(role__in=[UserEnum.OWNER, UserEnum.MEMBER, UserEnum.ADMIN])

    def get_admins(self):
        """Get all employees with roles 'ADMIN' for this company."""
        return self.employeemodel_set.filter(role__in=[UserEnum.ADMIN.value])

    def __str__(self):
        return self.name
