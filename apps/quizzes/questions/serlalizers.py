from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.answers.serializers import AnswerSerializer
from apps.quizzes.questions.models import QuestionModel


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuestionModel
        fields = ('id', 'question_text', 'answers')

    @transaction.atomic
    def create(self, validated_data):
        answers = validated_data.pop('answers')
        if len(answers) < 2:
            raise serializers.ValidationError({'detail': 'Each question must have at least two answer options'})

        question = QuestionModel.objects.create(**validated_data)

        correct_count = sum(1 for answer in answers if answer.get('is_correct'))
        if correct_count != 1:
            raise serializers.ValidationError({'detail': 'Each question must have exactly one correct answer'})
        for answer in answers:
            answer['question'] = question
            AnswerModel.objects.create(**answer)
        return question
