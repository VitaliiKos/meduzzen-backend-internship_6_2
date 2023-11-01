from django.db import models

from apps.quizzes.questions.models import QuestionModel


class AnswerModel(models.Model):
    class Meta:
        db_table = 'answers'
        ordering = ('id',)

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(default=False)
