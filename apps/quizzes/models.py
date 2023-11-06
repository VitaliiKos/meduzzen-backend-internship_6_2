from django.contrib.auth import get_user_model
from django.db import models

from apps.companies.models import CompanyModel
from apps.health_check.models import TimeStampedModel
from apps.users.models import UserModel as User

from .managers import QuizManager

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

    objects = QuizManager.as_manager()


class QuestionModel(models.Model):
    class Meta:
        db_table = 'questions'
        ordering = ('id',)

    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()


class AnswerModel(models.Model):
    class Meta:
        db_table = 'answers'
        ordering = ('id',)

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(default=False)
