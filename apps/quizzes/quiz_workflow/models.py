from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Max

from apps.companies.models import CompanyModel
from apps.health_check.models import TimeStampedModel
from apps.users.models import UserModel as User
from core.enums.quiz_result_enum import QuizResultEnum

from ..models import QuizModel

UserModel: User = get_user_model()


class QuizResultModel(TimeStampedModel):
    class Meta:
        db_table = 'quiz_result'
        ordering = ('-created_at',)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    total_question = models.IntegerField(default=0)
    total_answer = models.IntegerField(default=0)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(choices=[(status.value, status) for status in QuizResultEnum],
                              default=QuizResultEnum.STARTED.value)
    attempt = models.JSONField(blank=True, null=True, default=dict)

    @classmethod
    def get_system_rating(cls, user):
        user_system_rating = (cls.objects
                              .values("quiz")
                              .annotate(max_created_at=Max('created_at'))
                              .filter(user=user)
                              .aggregate(average_rating=Avg("score"))
                              )
        if user_system_rating['average_rating'] is not None:
            return round(user_system_rating['average_rating'], 2)
        else:
            return 0.0
    @classmethod
    def get_company_rating(cls, user, company):
        user_company_rating = (cls.objects
                               .values("quiz")
                               .annotate(max_created_at=Max('created_at'))
                               .filter(user=user, company=company)
                               .aggregate(average_rating=Avg("score"))
                               )

        if user_company_rating['average_rating'] is not None:
            return round(user_company_rating['average_rating'], 2)
        else:
            return 0.0
