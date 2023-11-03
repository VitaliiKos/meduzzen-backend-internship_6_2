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

        question_objects = []
        answers_data = None

        for question_data in questions:
            answers_data = question_data.pop('answers')
            if len(answers_data) < 2:
                raise serializers.ValidationError({'detail': 'Each question must have at least two answer options'})

            correct_count = sum(1 for answer in answers_data if answer.get('is_correct'))
            if correct_count != 1:
                raise serializers.ValidationError({'detail': 'Each question must have exactly one correct answer'})

            question_data['quiz'] = quiz
            question_objects.append(QuestionModel(**question_data))

        questions_bulk = QuestionModel.objects.bulk_create(question_objects)

        for i, question in enumerate(questions_bulk):
            for answer in answers_data[i * len(answers_data):(i + 1) * len(answers_data)]:
                answer['question'] = question

        answer_objects = [AnswerModel(**answer_data) for answer_data in answers_data]
        AnswerModel.objects.bulk_create(answer_objects)

        return quiz
