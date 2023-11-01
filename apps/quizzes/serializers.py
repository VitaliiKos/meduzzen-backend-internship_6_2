from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.models import QuizModel
from apps.quizzes.questions.models import QuestionModel
from apps.quizzes.questions.serlalizers import QuestionSerializer


class QuizSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuizModel
        fields = ('id', 'title', 'description', 'frequency', 'questions')
        order_by = ('-created_at',)

    @transaction.atomic
    def create(self, validated_data):
        questions = validated_data.pop('questions')
        if len(questions) < 2:
            raise serializers.ValidationError({'detail': 'There must be at least two questions'})

        quiz = QuizModel.objects.create(**validated_data)

        for question_data in questions:
            answers_data = question_data.pop('answers')
            if len(answers_data) < 2:
                raise serializers.ValidationError({'detail': 'Each question must have at least two answer options'})

            correct_count = sum(1 for answer in answers_data if answer.get('is_correct'))
            if correct_count != 1:
                raise serializers.ValidationError({'detail': 'Each question must have exactly one correct answer'})

            question_data['quiz'] = quiz

            question = QuestionModel.objects.create(**question_data)
            for answer in answers_data:
                answer['question'] = question
                AnswerModel.objects.create(**answer)
        return quiz
