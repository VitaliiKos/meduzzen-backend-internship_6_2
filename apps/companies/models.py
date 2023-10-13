from django.contrib.auth import get_user_model
from django.db import models

from apps.health_check.models import TimeStampedModel

UserModel = get_user_model()


class CompanyModel(TimeStampedModel):
    """Model representing a company."""

    class Meta:
        db_table = 'company'
        ordering = ('created_at',)

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    visible = models.BooleanField(default=False)

    members = models.ManyToManyField(UserModel, through="EmployeeModel")

    def __str__(self):
        return self.name


class EmployeeModel(TimeStampedModel):
    """Model representing an employee's relationship with a company.

    This model defines the relationship between users and companies,
    including their invitation status, request status, and role.
    """

    class Meta:
        db_table = 'employee'
        ordering = ('-created_at',)

    ROLE_CHOICES = (
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)

    invitation_status = models.CharField(max_length=10, choices=ROLE_CHOICES)
    request_status = models.CharField(max_length=10, choices=ROLE_CHOICES)
    role = models.CharField(max_length=255, null=False)

