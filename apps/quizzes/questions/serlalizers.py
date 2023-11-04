from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.answers.serializers import AnswerSerializer
from apps.quizzes.helper import validate_min_items, validate_correct_answers
from apps.quizzes.questions.models import QuestionModel


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuestionModel
        fields = ('id', 'question_text', 'answers')

    @transaction.atomic
    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        validate_min_items(answers_data, {'detail': 'Each question must have at least two answer options'})
        validate_correct_answers(answers_data)

        question = QuestionModel.objects.create(**validated_data)
        answer_objects = [AnswerModel(question=question, **answer) for answer in answers_data]

        AnswerModel.objects.bulk_create(answer_objects)

        return question
