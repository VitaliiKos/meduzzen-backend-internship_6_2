from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.quizzes.helper import validate_min_items, create_questions
from apps.quizzes.models import QuizModel
from apps.quizzes.questions.serlalizers import QuestionSerializer


class QuizSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuizModel
        fields = ('id', 'title', 'description', 'frequency', 'questions')
        ordering = ('-created_at',)

    @transaction.atomic
    def create(self, validated_data):
        questions = validated_data.pop('questions')
        validate_min_items(questions, {'detail': 'There must be at least two questions'})

        quiz = QuizModel.objects.create(**validated_data)
        create_questions(quiz, questions)

        return quiz
