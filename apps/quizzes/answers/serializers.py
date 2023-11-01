from rest_framework.serializers import ModelSerializer

from apps.quizzes.answers.models import AnswerModel


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ('id', 'answer_text', 'is_correct')

