from django.contrib.auth import get_user_model
from django.db import models

from apps.companies.models import CompanyModel
from apps.health_check.models import TimeStampedModel
from core.enums.invite_enum import InviteEnum
from core.enums.request_enum import RequestEnum

UserModel = get_user_model()


class InviteModel(TimeStampedModel):
    class Meta:
        db_table = 'invite'
        ordering = ('-created_at',)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[(status.value, status) for status in InviteEnum],
                              default=None, null=True)


class RequestModel(TimeStampedModel):
    class Meta:
        db_table = 'request'
        ordering = ('-created_at',)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[(status.value, status) for status in RequestEnum],
                              default=None, null=True)

