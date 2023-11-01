from django.contrib.auth import get_user_model
from django.db import models

from apps.companies.models import CompanyModel
from apps.health_check.models import TimeStampedModel
from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class QuizModel(TimeStampedModel):
    class Meta:
        db_table = 'quiz'
        ordering = ('-created_at',)

    title = models.CharField(max_length=255)
    description = models.TextField()
    frequency = models.PositiveIntegerField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
