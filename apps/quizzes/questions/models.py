from django.db import models

from apps.quizzes.models import QuizModel


class QuestionModel(models.Model):

    class Meta:
        db_table = 'questions'
        ordering = ('id',)

    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
